"""
Compute cosine similarity between two embedded texts using OpenAI Embeddings API.

Embeds each text via OpenAI text-embedding-3-small and calculates
cosine similarity between the resulting vectors.
Requires OPENAI_API_KEY environment variable or explicit api_key parameter.
"""

from typing import Optional

from openai import OpenAI

from embed_text import embed_text
from embeddings_models import cosine_similarity, normalize_vector

OPENAI_MODEL = "text-embedding-3-small"
OPENAI_DEFAULT_DIMENSIONS = 1536


def similarity_score(
    text_a: str,
    text_b: str,
    api_key: Optional[str] = None,
    model: str = OPENAI_MODEL,
    dimensions: int = OPENAI_DEFAULT_DIMENSIONS,
    client: Optional[OpenAI] = None,
    normalize: bool = True,
) -> float:
    """
    Compute cosine similarity between two texts via OpenAI embeddings.

    Both texts are embedded using the same OpenAI model, then their
    cosine similarity is calculated.

    Args:
        text_a: First text string.
        text_b: Second text string.
        api_key: OpenAI API key. Falls back to OPENAI_API_KEY env var.
        model: OpenAI embedding model identifier.
        dimensions: Output vector dimensions.
        client: Pre-configured OpenAI client (optional).
        normalize: Whether to L2-normalize vectors before computing similarity.

    Returns:
        Cosine similarity score in [-1, 1].
    """
    response_a = embed_text(
        text=text_a,
        api_key=api_key,
        model=model,
        dimensions=dimensions,
        client=client,
    )
    response_b = embed_text(
        text=text_b,
        api_key=api_key,
        model=model,
        dimensions=dimensions,
        client=client,
    )

    vec_a = response_a.embedding
    vec_b = response_b.embedding

    if normalize:
        vec_a = normalize_vector(vec_a)
        vec_b = normalize_vector(vec_b)

    return cosine_similarity(vec_a, vec_b)


def similarity_score_from_vectors(
    vec_a: list,
    vec_b: list,
    normalize: bool = True,
) -> float:
    """
    Compute cosine similarity from pre-computed embedding vectors.

    Useful when embeddings are cached or stored.

    Args:
        vec_a: First embedding vector.
        vec_b: Second embedding vector.
        normalize: Whether to L2-normalize before computing similarity.

    Returns:
        Cosine similarity score.
    """
    if normalize:
        vec_a = normalize_vector(vec_a)
        vec_b = normalize_vector(vec_b)
    return cosine_similarity(vec_a, vec_b)
