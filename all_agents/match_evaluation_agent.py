from agents import Agent
from schemas import MatchEvaluation

MATCH_PROMPT = """
You are a job-matching assistant. Compare the resume to the job description and score their match.
Return JSON with: "match_score" (0-100), "skills_matched", "skills_missing", "summary".

{resume_and_job}
"""

match_evaluation_agent = Agent(
    name="MatchEvaluationAgent",
    instructions=MATCH_PROMPT,
    model="gpt-4o",
    output_type=MatchEvaluation,
)
