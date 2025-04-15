from agents import Agent
from schemas import ATSFeedback

ATS_PROMPT = """
You are an expert in resume screening systems. Analyze the following resume for potential issues that may cause problems with Applicant Tracking Systems (ATS).
Respond in JSON with keys: "issues", "recommendations", "score" (0-100).
Resume:
{resume}
"""

ats_compliance_agent = Agent(
    name="ATSComplianceAgent",
    instructions=ATS_PROMPT,
    model="gpt-4o",
    output_type=ATSFeedback,
)
