from all_agents import (
    ats_compliance_agent,
    resume_feedback_agent,
    match_evaluation_agent,
    resume_optimization_agent,
    cover_letter_agent,
    company_research_agent,
)

agents = {
    "ats": ats_compliance_agent,
    "feedback": resume_feedback_agent,
    "match": match_evaluation_agent,
    "optimize": resume_optimization_agent,
    "cover": cover_letter_agent,
    "research": company_research_agent,
}
