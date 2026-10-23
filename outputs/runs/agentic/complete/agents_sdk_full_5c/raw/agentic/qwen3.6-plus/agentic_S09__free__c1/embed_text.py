"""Generate an embedding vector for a single text string using OpenAI embeddings API."""

import os
import numpy as np
from openai import OpenAI

from embeddings_client import get_openai_client
from embeddings_models import EmbeddingRequest, EmbeddingResponse, normalize_vector


def embed_text(text: str, model: str = "text-embedding-3-small") -> EmbeddingResponse:
    """Generate an embedding vector for one text string.

    Uses OpenAI's text-embedding-3-small model by default.
    https://platform.openai.com/docs/guides/embeddings

    Args:
        text: The input text to embed.
        model: OpenAI embedding model identifier.

    Returns:
        EmbeddingResponse containing the vector and metadata.
    """
    client = get_openai_client()

    request = EmbeddingRequest(
        input=text,
        model=model,
        encoding_format="float",
    )

    response = client.embeddings.create(
        input=request.input,
        model=request.model,
        encoding_format=request.encoding_format,
    )

    raw_vector = response.data[0].embedding
    normalized_vector = normalize_vector(raw_vector)

    return EmbeddingResponse(
        vector=normalized_vector,
        model=response.model,
        usage=response.usage,
        raw_response=response,
    )


def get_embedding_array(text: str, model: str = "text-embedding-3-small") -> np.ndarray:
    """Return embedding as a numpy array for numerical operations."""
    response = embed_text(text, model=model)
    return np.array(response.vector, dtype=np.float32)


if __name__ == "__main__":
    sample_text = "OpenAI embeddings provide dense vector representations for text."
    result = embed_text(sample_text)
    print(f"Model: {result.model}")
    print(f"Vector dimension: {len(result.vector)}")
    print(f"First 5 values: {result.vector[:5]}")
