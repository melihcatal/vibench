"""
Generates embeddings for a batch of texts.

Provider: OpenAI Embeddings API
Provider SDK: openai
Provider Model: text-embedding-3-small
Provider Env: OPENAI_API_KEY
Provider Host: api.openai.com
"""

from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingRequest, EmbeddingResponse


def embed_batch(
    texts: list[str],
    model: str = "text-embedding-3-small",
    dimensions: int = 1536,
) -> EmbeddingResponse:
    """Generate embeddings for a batch of text strings using OpenAI.

    Args:
        texts: List of text strings to embed.
        model: OpenAI embedding model identifier (default: text-embedding-3-small).
        dimensions: Output embedding dimensions.

    Returns:
        EmbeddingResponse containing all embedding vectors.
    """
    request = EmbeddingRequest(texts=texts, model=model, dimensions=dimensions)
    client = EmbeddingsClient(model=request.model, dimensions=request.dimensions)
    embeddings = client.embed_many(texts=request.texts, dimensions=request.dimensions)
    return EmbeddingResponse(
        embeddings=embeddings,
        model=request.model,
    )


if __name__ == "__main__":
    texts = [
        "The quick brown fox jumps over the lazy dog.",
        "Machine learning models learn patterns from data.",
        "Embeddings represent text as dense vectors.",
    ]
    resp = embed_batch(texts)
    print(f"Model: {resp.model}")
    print(f"Batch size: {len(resp.embeddings)}")
    print(f"First embedding dimensions: {len(resp.embeddings[0])}")
