from collections import Counter

from openai import OpenAI


def embedding_job_summary(job_id: str):
    client = OpenAI()
    job = client.fine_tuning.jobs.retrieve(job_id)
    status_counts = Counter([getattr(job, "status", "unknown")])
    return {
        "job_id": job.id,
        "status": job.status,
        "status_counts": dict(status_counts),
    }
