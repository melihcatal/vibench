from embeddings_client import client
from embeddings_models import EmbeddingRequest, EmbeddingResponse


def embed_text(request: EmbeddingRequest) -> EmbeddingResponse:
    response = client.embeddings.create(
        input=request.text, model="text-embedding-3-small"
    )
    embedding = response.data[0].embedding
    return EmbeddingResponse(embedding=embedding)
