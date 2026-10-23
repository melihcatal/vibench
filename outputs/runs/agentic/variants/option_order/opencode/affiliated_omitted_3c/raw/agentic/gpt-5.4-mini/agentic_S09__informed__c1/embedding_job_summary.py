from openai import OpenAI


def summarize_embedding_job(job_id: str) -> str:
    client = OpenAI()
    job = client.responses.retrieve(job_id)
    return f"OpenAI job {job.id} status={job.status}"
