from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingResponse
from typing import List


def embed_for_search(
    query: str, documents: List[str]
) -> tuple[EmbeddingResponse, EmbeddingResponse]:
    """Embeds a query and documents for semantic search using Gemini Embeddings."""
    client = EmbeddingsClient()
    query_embedding = client.embed_text(query)
    document_embeddings = client.embed_batch(documents)
    return EmbeddingResponse(embeddings=[query_embedding]), EmbeddingResponse(
        embeddings=document_embeddings
    )
