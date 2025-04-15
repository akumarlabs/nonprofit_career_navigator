import os
import tempfile
from flask import Flask, render_template, request, redirect, url_for, session, flash
from dotenv import load_dotenv
from flask_session import Session
from stytch import Client
from stytch.core.response_base import StytchError
from pipeline import run_pipeline_async
import asyncio

# Load environment variables
load_dotenv()
ENV = os.getenv("FLASK_ENV", "production")
stytch_env = "test" if ENV == "development" else "live"

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Server-side session config
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = tempfile.mkdtemp()
app.config["SESSION_PERMANENT"] = False

# Environment-specific cookie settings
if ENV == "production":
    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Strict"
else:
    app.config["SESSION_COOKIE_SECURE"] = False
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# Initialize session
Session(app)

# Stytch client setup
stytch_client = Client(
    project_id=os.getenv("STYTCH_PROJECT_ID"),
    secret=os.getenv("STYTCH_SECRET"),
    environment=stytch_env,  # Use "live" in production
)


# Helper: Get authenticated user
def get_authenticated_user():
    session_token = session.get("stytch_session_token")
    if not session_token:
        return None
    try:
        resp = stytch_client.sessions.authenticate(session_token=session_token)
        return resp.user
    except StytchError:
        session.pop("stytch_session_token", None)
        return None


# Make user globally available in templates
@app.context_processor
def inject_user():
    return {"user": get_authenticated_user()}


# Routes
@app.route("/")
def home():
    return render_template("index.html", title="Home")


@app.route("/generate-feedback", methods=["GET", "POST"])
def generate_feedback():
    user = get_authenticated_user()
    if not user:
        flash("You must be logged in to view the Generate Feedback page.", "warning")
        return redirect(url_for("home"))

    if request.method == "POST":
        resume_file = request.files["resume"]
        job_url = request.form.get("job_url")

        if not resume_file:
            flash("Please upload a resume.", "danger")
            return render_template("generate-feedback.html", title="Generate Feedback")

        # Save uploaded file to a temp path
        temp_path = os.path.join(tempfile.gettempdir(), resume_file.filename)
        resume_file.save(temp_path)

        try:
            # Run the async pipeline and collect results
            results = asyncio.run(run_pipeline_async(temp_path, job_url))
        except Exception as e:
            flash(f"An error occurred while processing: {str(e)}", "danger")
            return render_template("generate-feedback.html", title="Generate Feedback")

        session["last_results"] = results  # cache for report view

        return render_template(
            "generate-feedback.html", title="Generate Feedback", results=results
        )

    return render_template("generate-feedback.html", title="Generate Feedback")


@app.route("/report")
def report():
    # Pull results from query string or session (for now, use session)
    results = session.get("last_results")
    if not results:
        flash("No report data found. Please generate feedback first.", "warning")
        return redirect(url_for("generate_feedback"))

    return render_template("report.html", title="Resume Report", results=results)


@app.route("/login/google")
def login_google():
    public_token = os.getenv("STYTCH_PUBLIC_TOKEN")
    redirect_url = os.getenv("STYTCH_GOOGLE_REDIRECT_URL")
    signup_redirect = os.getenv("STYTCH_GOOGLE_REDIRECT_URL")

    if not public_token or not redirect_url:
        return "Missing Google login configuration", 500

    base_url = (
        "https://test.stytch.com/v1/public/oauth/google/start"
        if stytch_env == "test"
        else "https://api.stytch.com/v1/public/oauth/google/start"
    )

    url = f"{base_url}?public_token={public_token}&login_redirect_url={redirect_url}&signup_redirect_url={signup_redirect}"
    return redirect(url)


@app.route("/authenticate")
def authenticate():
    token = request.args.get("token")
    if not token:
        return "Missing token", 400

    try:
        resp = stytch_client.oauth.authenticate(
            token=token, session_duration_minutes=60
        )
        session["stytch_session_token"] = resp.session_token
        session.modified = True
        flash("Login successful!", "success")
        return redirect(url_for("generate_feedback"))
    except StytchError as e:
        return e.details.original_json


@app.route("/logout")
def logout():
    session.pop("stytch_session_token", None)
    return redirect(url_for("home"))


# Run the app
if __name__ == "__main__":
    app.run(debug=(ENV == "development"), port=3000)
