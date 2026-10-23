"""Generates an embedding vector for one text string using OpenAI Embeddings API.

Uses the text-embedding-3-small model from OpenAI to produce a single embedding.
"""

import os
from typing import List

from embeddings_client import get_openai_client, create_embedding, get_embedding_model
from embeddings_models import EmbeddingRequest


def embed_single_text(text: str, model: str = None, dimensions: int = None) -> List[float]:
    """Generate an embedding vector for one text string.

    Args:
        text: Input text to embed.
        model: OpenAI embedding model ID (defaults to OPENAI_EMBEDDING_MODEL env var
               or text-embedding-3-small).
        dimensions: Optional output dimensionality.

    Returns:
        List of floats representing the embedding vector.
    """
    client = get_openai_client()
    model_id = model or get_embedding_model()

    request = EmbeddingRequest(
        texts=[text],
        model=model_id,
        dimensions=dimensions,
    )

    embedding = create_embedding(
        client=client,
        text=text,
        model=model_id,
        dimensions=dimensions,
    )

    return embedding


def main():
    text = os.environ.get("EMBED_TEXT", "The quick brown fox jumps over the lazy dog")
    model = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    dimensions_str = os.environ.get("EMBED_DIMENSIONS", None)
    dimensions = int(dimensions_str) if dimensions_str else None

    embedding = embed_single_text(text, model=model, dimensions=dimensions)
    print(f"Model: {model}")
    print(f"Text: {text}")
    print(f"Embedding dimension: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")


if __name__ == "__main__":
    main()
