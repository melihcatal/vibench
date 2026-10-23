from embeddings_client import DirectEmbeddingsClient


def embedding_job_summary(job_id, config=None):
    client = DirectEmbeddingsClient(config)
    summary = client.get_job_summary(job_id)
    return {"summary": summary}