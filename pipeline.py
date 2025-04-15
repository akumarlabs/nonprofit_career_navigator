import asyncio
import logging
from tools import ResumeParser, JobDescriptionParser
from manager import agents
from agents import Runner


async def run_agent_debug(agent_key: str, input_payload):
    try:
        agent = agents[agent_key]
        #print("✅ Agent Type:", type(agent))
        #print("📄 Instructions Snippet:", agent.instructions[:300])
        #print(
        #    "🔍 Placeholder Found:",
        #    "{resume" in agent.instructions or "{input" in agent.instructions,
        #)
        result = await Runner.run(agent, input=input_payload)
        return result
    except Exception:
        logging.exception(f"❌ Agent '{agent_key}' failed with input: {input_payload}")
        raise


async def run_pipeline_async(resume_path: str, job_source: str = None) -> dict:
    resume_text = ResumeParser()(resume_path)
    job_description = await JobDescriptionParser()(job_source) if job_source else ""
    results = {}

    # Run resume-only agents
    resume_tasks = await asyncio.gather(
        run_agent_debug("ats", resume_text),
        run_agent_debug("feedback", resume_text),
    )
    results.update(
        {
            "ATS Feedback": resume_tasks[0].final_output.model_dump(),
            "Resume Feedback": resume_tasks[1].final_output.model_dump(),
        }
    )

    if job_description:
        resume_and_job_input = f"""Resume:
{resume_text}

Job Description:
{job_description}"""

        job_tasks = await asyncio.gather(
            run_agent_debug("match", resume_and_job_input),
            run_agent_debug("optimize", resume_and_job_input),
            run_agent_debug("cover", resume_and_job_input),
            run_agent_debug("research", job_description),
        )

        results.update(
            {
                "Match Evaluation": job_tasks[0].final_output.model_dump(),
                "Resume Optimization": job_tasks[1].final_output.model_dump(),
                "Cover Letter Advice": job_tasks[2].final_output.model_dump(),
                "Company Research": job_tasks[3].final_output.model_dump(),
            }
        )

    return results
