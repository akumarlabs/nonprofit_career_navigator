from agents import Agent
from schemas import ResumeFeedback

FEEDBACK_PROMPT = """
You are a career coach. Provide general feedback on this resume including formatting, tone, grammar, and effectiveness.
Return JSON with: "strengths", "areas_to_improve", "overall_assessment".
Resume:
{resume}
"""

resume_feedback_agent = Agent(
    name="ResumeFeedbackAgent",
    instructions=FEEDBACK_PROMPT,
    model="gpt-4o",
    output_type=ResumeFeedback,
)
