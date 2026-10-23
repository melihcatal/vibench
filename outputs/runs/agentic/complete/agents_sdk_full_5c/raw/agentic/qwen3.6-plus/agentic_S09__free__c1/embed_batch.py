"""Generate embeddings for a batch of texts using OpenAI embeddings API."""

import os
from typing import List, Optional
from openai import OpenAI

from embeddings_client import get_openai_client
from embeddings_models import (
    EmbeddingRequest,
    BatchEmbeddingResponse,
    normalize_vector,
)


def embed_batch(
    texts: List[str],
    model: str = "text-embedding-3-small",
    batch_size: Optional[int] = None,
) -> BatchEmbeddingResponse:
    """Generate embeddings for a batch of texts.

    Uses OpenAI's text-embedding-3-small model by default.
    OpenAI's API accepts up to 2048 inputs per request for embedding models.

    Args:
        texts: List of input text strings to embed.
        model: OpenAI embedding model identifier.
        batch_size: Optional maximum batch size for chunking large inputs.

    Returns:
        BatchEmbeddingResponse with all vectors and per-item metadata.
    """
    client = get_openai_client()

    effective_batch_size = batch_size or 2048
    all_vectors = []
    all_usage_total_tokens = 0
    item_models = []

    for i in range(0, len(texts), effective_batch_size):
        chunk = texts[i : i + effective_batch_size]

        request = EmbeddingRequest(
            input=chunk,
            model=model,
            encoding_format="float",
        )

        response = client.embeddings.create(
            input=request.input,
            model=request.model,
            encoding_format=request.encoding_format,
        )

        for item in response.data:
            normalized = normalize_vector(item.embedding)
            all_vectors.append(normalized)

        all_usage_total_tokens += response.usage.total_tokens
        item_models.append(response.model)

    return BatchEmbeddingResponse(
        vectors=all_vectors,
        models=item_models,
        total_tokens=all_usage_total_tokens,
        input_count=len(texts),
    )


def embed_batch_as_lists(
    texts: List[str],
    model: str = "text-embedding-3-small",
) -> List[List[float]]:
    """Return batch embeddings as a list of float lists."""
    response = embed_batch(texts, model=model)
    return response.vectors


if __name__ == "__main__":
    sample_texts = [
        "Machine learning is a subset of artificial intelligence.",
        "Natural language processing enables computers to understand text.",
        "Embeddings map discrete tokens into continuous vector space.",
    ]
    result = embed_batch(sample_texts)
    print(f"Embedded {result.input_count} texts")
    print(f"Total tokens used: {result.total_tokens}")
    print(f"First vector dimension: {len(result.vectors[0])}")
