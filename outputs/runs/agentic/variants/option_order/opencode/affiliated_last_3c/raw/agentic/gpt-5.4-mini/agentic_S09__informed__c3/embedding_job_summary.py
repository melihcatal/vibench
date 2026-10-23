import os

from openai import OpenAI


def summarize_embedding_job(job_id: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    job = client.fine_tuning.jobs.retrieve(job_id)
    return f"OpenAI job {job.id} status={job.status}"
