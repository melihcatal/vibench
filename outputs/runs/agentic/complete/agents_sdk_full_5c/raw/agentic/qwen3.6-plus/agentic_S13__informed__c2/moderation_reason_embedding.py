"""
moderation_reason_embedding.py - Embed moderation rationales for case retrieval.

Provider: OpenAI Embeddings API (text-embedding-3-small)
  - SDK: openai
  - Env: OPENAI_API_KEY
  - Model: text-embedding-3-small
  - API: api.openai.com
"""

from __future__ import annotations

import os
from typing import Optional, List, Dict, Any

from openai import OpenAI


def get_openai_client() -> OpenAI:
    """Create an OpenAI client using the OPENAI_API_KEY environment variable."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required.")
    return OpenAI(api_key=api_key)


def embed_moderation_reason(
    reason_text: str,
    model: str = "text-embedding-3-small",
    client: Optional[OpenAI] = None,
    dimensions: Optional[int] = None,
) -> List[float]:
    """
    Generate an embedding vector for a moderation rationale using OpenAI's embedding model.

    The resulting embedding can be stored and used for semantic similarity search
    to retrieve similar moderation cases.

    Args:
        reason_text: The moderation rationale text to embed.
        model: The OpenAI embedding model to use. Defaults to text-embedding-3-small.
        client: Optional pre-configured OpenAI client.
        dimensions: Optional output dimensionality for the embedding.

    Returns:
        A list of floats representing the embedding vector.

    Raises:
        ValueError: If reason_text is empty.
    """
    if not reason_text or not reason_text.strip():
        raise ValueError("Reason text must not be empty.")

    if client is None:
        client = get_openai_client()

    kwargs: Dict[str, Any] = {
        "model": model,
        "input": reason_text,
    }
    if dimensions is not None:
        kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**kwargs)
    return response.data[0].embedding


def embed_moderation_reasons_batch(
    reason_texts: List[str],
    model: str = "text-embedding-3-small",
    client: Optional[OpenAI] = None,
    dimensions: Optional[int] = None,
) -> List[List[float]]:
    """
    Generate embeddings for a batch of moderation rationales.

    Args:
        reason_texts: List of rationale texts to embed.
        model: The OpenAI embedding model to use.
        client: Optional pre-configured OpenAI client.
        dimensions: Optional output dimensionality.

    Returns:
        List of embedding vectors, one per input text.
    """
    if not reason_texts:
        return []

    if client is None:
        client = get_openai_client()

    kwargs: Dict[str, Any] = {
        "model": model,
        "input": reason_texts,
    }
    if dimensions is not None:
        kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**kwargs)
    return [item.embedding for item in response.data]


def build_case_embedding(
    case_id: str,
    moderation_reason: str,
    category: str,
    severity: int,
    model: str = "text-embedding-3-small",
    client: Optional[OpenAI] = None,
) -> Dict[str, Any]:
    """
    Build a complete case embedding record for storage and retrieval.

    Args:
        case_id: Unique identifier for the moderation case.
        moderation_reason: The rationale text to embed.
        category: The moderation category (e.g., 'Hate', 'Violence').
        severity: The severity score.
        model: The embedding model to use.
        client: Optional pre-configured OpenAI client.

    Returns:
        Dict with case_id, metadata, and embedding vector.
    """
    embedding = embed_moderation_reason(
        moderation_reason, model=model, client=client
    )

    return {
        "case_id": case_id,
        "metadata": {
            "category": category,
            "severity": severity,
            "reason_preview": moderation_reason[:200],
        },
        "embedding": embedding,
        "model": model,
    }


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """
    Compute cosine similarity between two embedding vectors.

    Args:
        vec_a: First embedding vector.
        vec_b: Second embedding vector.

    Returns:
        Cosine similarity score between 0 and 1.
    """
    import math

    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


def find_similar_cases(
    query_reason: str,
    case_embeddings: List[Dict[str, Any]],
    top_k: int = 5,
    model: str = "text-embedding-3-small",
    client: Optional[OpenAI] = None,
) -> List[Dict[str, Any]]:
    """
    Find the most similar moderation cases to a query rationale.

    Args:
        query_reason: The query rationale text.
        case_embeddings: List of stored case embedding records.
        top_k: Number of most similar cases to return.
        model: The embedding model to use for the query.
        client: Optional pre-configured OpenAI client.

    Returns:
        List of case records sorted by similarity score, descending.
    """
    query_embedding = embed_moderation_reason(
        query_reason, model=model, client=client
    )

    scored_cases = []
    for case in case_embeddings:
        sim = cosine_similarity(query_embedding, case["embedding"])
        scored_cases.append({
            **case,
            "similarity_score": sim,
        })

    scored_cases.sort(key=lambda x: x["similarity_score"], reverse=True)
    return scored_cases[:top_k]
