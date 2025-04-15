from agents import Agent
from schemas import CoverLetterAdvice

COVER_PROMPT = """
You are a career coach. Based on the resume and job description, suggest whether a cover letter is needed and what to include.
Return JSON with: "is_cover_letter_needed" (true/false), "key_points_to_include", "tone_suggestions".

{resume_and_job}
"""

cover_letter_agent = Agent(
    name="CoverLetterAgent",
    instructions=COVER_PROMPT,
    model="gpt-4o",
    output_type=CoverLetterAdvice,
)
