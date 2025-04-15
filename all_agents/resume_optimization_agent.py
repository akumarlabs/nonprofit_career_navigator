from agents import Agent
from schemas import ResumeOptimization

OPTIMIZE_PROMPT = """
You are an expert resume optimizer. Suggest how the resume can be improved to better match the job description.
Return JSON with: "recommended_changes", "sections_to_update", "rationale".

{resume_and_job}
"""

resume_optimization_agent = Agent(
    name="ResumeOptimizationAgent",
    instructions=OPTIMIZE_PROMPT,
    model="gpt-4o",
    output_type=ResumeOptimization,
)
