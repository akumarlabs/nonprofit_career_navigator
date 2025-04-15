from agents import Agent
from schemas import CompanyResearch

RESEARCH_PROMPT = """
You are a company research analyst. Based on this job description, provide 3 insightful questions the candidate could ask in an interview.
Return JSON with: "company_insights", "suggested_questions".
Job Description:
{job}
"""

company_research_agent = Agent(
    name="CompanyResearchAgent",
    instructions=RESEARCH_PROMPT,
    model="gpt-4o",
    output_type=CompanyResearch,
)
