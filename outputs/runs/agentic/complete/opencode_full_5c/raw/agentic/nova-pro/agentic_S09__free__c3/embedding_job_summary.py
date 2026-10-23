import os

from embeddings_client import DirectEmbeddingsClient


def summarize_embedding_job_results(job_id: str) -> str:
    client = DirectEmbeddingsClient()
    response = client.get_job_results(job_id)
    return response.summary
