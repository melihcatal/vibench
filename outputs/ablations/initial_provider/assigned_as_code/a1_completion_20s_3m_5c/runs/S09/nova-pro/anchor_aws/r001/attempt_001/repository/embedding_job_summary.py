from embeddings_client import get_bedrock_client
from embeddings_models import EmbeddingRequest, EmbeddingResponse


def embedding_job_summary(job_id, config=None):
    config = config or {}
    client = get_bedrock_client(config)
    response = client.get_embedding_job(jobId=job_id)
    return response["summary"]