from openai import OpenAI


def embedding_job_summary(job_id: str):
    client = OpenAI(api_key=None)
    return {
        "job_id": job_id,
        "provider": "openai",
        "status": "submitted",
        "client": type(client).__name__,
    }
