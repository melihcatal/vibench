from embeddings_client import EmbeddingsClient

client = EmbeddingsClient()


def summarize_embedding_job(job_id: str) -> str:
    response = client.summarize_job(job_id)
    return response["summary"]
