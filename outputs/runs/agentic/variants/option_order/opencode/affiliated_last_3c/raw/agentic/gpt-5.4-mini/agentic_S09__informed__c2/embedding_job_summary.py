from openai import OpenAI


def embedding_job_summary(job_result):
    client = OpenAI(api_key=None)
    count = len(job_result.get("embeddings", []))
    return {
        "provider": "openai",
        "embedding_count": count,
        "job_id": job_result.get("job_id"),
    }
