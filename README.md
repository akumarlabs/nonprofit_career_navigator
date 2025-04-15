# Nonprofit Career Navigator

## 🚀 Overview

**Nonprofit Career Navigator** is a Flask-based web application that leverages multiple AI agents to help job seekers in the social impact sector improve their resumes, tailor their applications, and write more compelling cover letters.

Whether you're applying to nonprofit, government, or foundation roles, this tool streamlines the process by analyzing your resume and the job description - and providing intelligent, targeted feedback.

---

## ✨ Features

- **Upload & Analyze**: Upload your resume and paste a job URL. Let the system take over.
- **ATS Compliance Report**: Evaluate how Applicant Tracking System - friendly your resume is.
- **Detailed Resume Feedback**: Language, tone, formatting, clarity, and more.
- **Match Evaluation**: See how well your resume aligns with the job description.
- **Resume Optimization Suggestions**: Targeted improvements based on the job description.
- **Cover Letter Advice**: AI-generated suggestions and templates for your cover letter.
- **Company Research Agent**: Key facts and tips based on the organization behind the job.

---

## 🧱 Tech Stack

- **Backend**: Python 3.10, Flask, Gunicorn
- **Frontend**: Jinja2 templates, Bootstrap 5
- **AI Agents**: Modular async agents powered by a shared Runner interface
- **Parsing Tools**: `pdfplumber`, `python-docx`, `BeautifulSoup`, `Playwright`
- **Authentication**: [Stytch](https://stytch.com) for Google OAuth

---

## 🖥️ How It Works

1. **User logs in via Google**
2. **Uploads a resume (PDF or DOCX)**
3. **Enters a job description URL**
4. **Pipeline runs asynchronously**:
   - Resume is parsed
   - Job description is extracted (via `requests` or Playwright)
   - Agents are run to generate analysis
5. **A detailed report is generated**, including match score, suggestions, and more.

---

## 🛠 Installation

### 1. Clone the repository
```bash
git clone https://github.com/akumarlabs/nonprofit_career_navigator.git
cd nonprofit_career_navigator
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. (Optional) Install Playwright for job parsing
```bash
pip install playwright
playwright install --with-deps
```

---

## 🧪 Running Locally

```bash
python app.py
```

Then open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 🧩 Project Structure

```
nonprofit_career_navigator/
├── agents/
│   ├── ats_compliance_agent.py
│   ├── company_research_agent.py
│   └── ...
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── generate-feedback.html
│   └── report.html
├── app.py
├── tools.py
├── pipeline.py
├── manager.py
├── schemas.py
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🔒 Security Considerations

- Google login is handled securely via [Stytch](https://stytch.com)
- No resume or job data is persisted
- Input validation for uploaded files and URLs
- Playwright runs headless Chromium in sandboxed container environments

---

## 🛣 Future Enhancements

- Alerts
- Cloud storage for past analyses
- More career-sector-specific tuning

---

## 🙌 Contributing

1. Fork the repo
2. Create a new branch: `git checkout -b my-feature`
3. Commit your changes: `git commit -m 'Add cool feature'`
4. Push: `git push origin my-feature`
5. Open a Pull Request

---

## 📄 License

MIT License  
© 2025 Anand Kumar
