"""
Embed moderation rationales for case retrieval.
Provider: OpenAI Embeddings API
"""

import os
from typing import Optional, List, Dict

from openai import OpenAI


DEFAULT_MODEL = "text-embedding-3-small"


def _get_openai_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key)


def embed_moderation_rationale(
    rationale: str,
    model: str = DEFAULT_MODEL,
    dimensions: Optional[int] = None,
) -> List[float]:
    """
    Embed a single moderation rationale using OpenAI's text-embedding-3-small model.

    Args:
        rationale: The rationale text to embed (e.g. moderation reason).
        model: OpenAI embedding model identifier.
        dimensions: Optional output dimensionality for the embedding.

    Returns:
        List of float values representing the embedding vector.
    """
    client = _get_openai_client()

    kwargs: Dict = {}
    if dimensions:
        kwargs["dimensions"] = dimensions

    response = client.embeddings.create(
        model=model,
        input=rationale,
        **kwargs,
    )

    return response.data[0].embedding


def embed_moderation_rationales(
    rationales: List[str],
    model: str = DEFAULT_MODEL,
    dimensions: Optional[int] = None,
) -> List[List[float]]:
    """
    Embed a batch of moderation rationales using OpenAI embeddings API.

    Args:
        rationales: List of rationale texts to embed.
        model: OpenAI embedding model identifier.
        dimensions: Optional output dimensionality.

    Returns:
        List of embedding vectors.
    """
    client = _get_openai_client()

    kwargs: Dict = {}
    if dimensions:
        kwargs["dimensions"] = dimensions

    response = client.embeddings.create(
        model=model,
        input=rationales,
        **kwargs,
    )

    return [item.embedding for item in response.data]


def embed_with_metadata(
    rationale: str,
    case_id: str,
    model: str = DEFAULT_MODEL,
    dimensions: Optional[int] = None,
) -> Dict:
    """
    Embed a moderation rationale and attach case metadata.

    Args:
        rationale: The rationale text to embed.
        case_id: Identifier for the moderation case.
        model: OpenAI embedding model identifier.
        dimensions: Optional output dimensionality.

    Returns:
        Dict with embedding, case_id, model, and text.
    """
    embedding = embed_moderation_rationale(rationale, model=model, dimensions=dimensions)

    return {
        "case_id": case_id,
        "rationale": rationale,
        "embedding": embedding,
        "model": model,
        "dimensions": len(embedding),
    }
