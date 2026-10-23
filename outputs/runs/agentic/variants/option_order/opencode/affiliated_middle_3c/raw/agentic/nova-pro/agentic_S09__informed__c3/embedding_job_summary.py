from openai import OpenAI

client = OpenAI()


def summarize_embedding_job(job_id: str) -> str:
    response = client.embeddings.retrieve(job_id)
    return f"Summary of job {job_id}: {response.status}"
