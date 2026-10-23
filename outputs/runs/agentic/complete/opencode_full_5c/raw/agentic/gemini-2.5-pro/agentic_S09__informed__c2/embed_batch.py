from embeddings_client import client
from embeddings_models import BatchEmbeddingRequest, BatchEmbeddingResponse


def embed_batch(request: BatchEmbeddingRequest) -> BatchEmbeddingResponse:
    response = client.embeddings.create(
        input=request.texts, model="text-embedding-3-small"
    )
    embeddings = [item.embedding for item in response.data]
    return BatchEmbeddingResponse(embeddings=embeddings)
