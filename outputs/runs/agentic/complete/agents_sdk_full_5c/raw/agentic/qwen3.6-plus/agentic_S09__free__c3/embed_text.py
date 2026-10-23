"""
Generates an embedding vector for one text string.

Provider: OpenAI Embeddings API
Provider SDK: openai
Provider Model: text-embedding-3-small
Provider Env: OPENAI_API_KEY
Provider Host: api.openai.com
"""

from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingRequest, EmbeddingResponse


def embed_text(text: str, model: str = "text-embedding-3-small", dimensions: int = 1536) -> EmbeddingResponse:
    """Generate an embedding vector for a single text string using OpenAI.

    Args:
        text: The text to embed.
        model: OpenAI embedding model identifier (default: text-embedding-3-small).
        dimensions: Output embedding dimensions.

    Returns:
        EmbeddingResponse containing the embedding vector.
    """
    request = EmbeddingRequest(text=text, model=model, dimensions=dimensions)
    client = EmbeddingsClient(model=request.model, dimensions=request.dimensions)
    embedding = client.embed(text=request.text, dimensions=request.dimensions)
    return EmbeddingResponse(
        embedding=embedding,
        model=request.model,
        usage={},
    )


if __name__ == "__main__":
    resp = embed_text("Hello, world!")
    print(f"Model: {resp.model}")
    print(f"Dimensions: {len(resp.embedding)}")
    print(f"First 5 values: {resp.embedding[:5]}")
