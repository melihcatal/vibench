"""
embed_text.py - Generates an embedding vector for one text string.

Provider: OpenAI Embeddings API
Model: text-embedding-3-small
SDK: openai
Auth: OPENAI_API_KEY
"""

import os
import sys

from embeddings_client import get_openai_client, resolve_model
from embeddings_models import EmbeddingRequest, EmbeddingVector, parse_openai_embedding_response


def embed_single_text(
    text: str,
    model: str | None = None,
    dimensions: int | None = None,
) -> EmbeddingVector:
    """Generate an embedding vector for a single text string via OpenAI Embeddings API.

    Args:
        text: The input text to embed.
        model: OpenAI embedding model identifier (default: text-embedding-3-small).
        dimensions: Optional output dimensionality for the embedding vector.

    Returns:
        An EmbeddingVector containing the dense representation.
    """
    client = get_openai_client()
    resolved_model = resolve_model(model)

    request = EmbeddingRequest(
        input=text,
        model=resolved_model,
        dimensions=dimensions,
    )

    response = client.embeddings.create(**request.to_openai_params())
    parsed = parse_openai_embedding_response(response)

    vector = parsed.get_vector(0)
    if vector is None:
        raise RuntimeError("No embedding vector returned from OpenAI Embeddings API")
    return vector


def main() -> None:
    text = sys.argv[1] if len(sys.argv) > 1 else "Hello, world! This is a test embedding."
    model = os.environ.get("OPENAI_EMBEDDING_MODEL", None)

    result = embed_single_text(text, model=model)
    print(f"Model: {result.model or 'text-embedding-3-small'}")
    print(f"Dimensionality: {len(result.vector)}")
    print(f"First 5 values: {result.vector[:5]}")


if __name__ == "__main__":
    main()
