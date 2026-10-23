from openai import OpenAI

from embeddings_client import get_api_key, get_embedding_model


def embedding_job_summary(job_id: str):
    client = OpenAI(api_key=get_api_key())
    model = get_embedding_model()
    return {
        "job_id": job_id,
        "model": model,
        "status": "summarized",
        "provider": "openai",
    }
