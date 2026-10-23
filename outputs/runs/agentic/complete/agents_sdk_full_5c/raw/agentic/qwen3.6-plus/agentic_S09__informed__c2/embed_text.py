"""
Same-scenario: Generate an embedding vector for one text string.
Provider: OpenAI Embeddings API via openai SDK.
Auth: OPENAI_API_KEY
Model: text-embedding-3-small
"""

from typing import List, Optional

from embeddings_client import create_embeddings_client, DEFAULT_EMBEDDING_MODEL
from embeddings_models import EmbeddingRequest, EmbeddingResponse, parse_openai_embedding_response


def embed_text(
    text: str,
    model: Optional[str] = None,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
) -> EmbeddingResponse:
    """Generate an embedding vector for a single text string using OpenAI.

    Args:
        text: The input text to embed.
        model: OpenAI embedding model identifier (default: text-embedding-3-small).
        dimensions: Optional output dimensionality for the embedding.
        api_key: Optional override for OPENAI_API_KEY.

    Returns:
        EmbeddingResponse with the embedding vector and metadata.
    """
    resolved_model = model or DEFAULT_EMBEDDING_MODEL
    client = create_embeddings_client(api_key=api_key)

    request = EmbeddingRequest(
        text=text,
        model=resolved_model,
        dimensions=dimensions,
    )

    raw_response = client.embeddings.create(**request.to_openai_kwargs())
    return parse_openai_embedding_response(raw_response, index=0)


if __name__ == "__main__":
    result = embed_text("Hello world, this is a test embedding.")
    print(f"Model: {result.model}")
    print(f"Vector length: {len(result.embedding)}")
    print(f"First 5 dims: {result.embedding[:5]}")
