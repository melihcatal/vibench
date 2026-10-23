"""Embed translated segments for translation-memory search using hosted embeddings.

Provider: OpenAI Embeddings API (openai SDK)
Model: text-embedding-3-small
Auth: OPENAI_API_KEY
"""

from __future__ import annotations

import os
from typing import Optional

import openai


MODEL_ID = "text-embedding-3-small"


def embed_segment(
    text: str,
    model: str = MODEL_ID,
    api_key: Optional[str] = None,
) -> list[float]:
    """Embed a single translated segment via OpenAI Embeddings API.

    Args:
        text: The text segment to embed (e.g. a translated sentence).
        model: OpenAI embedding model (default: text-embedding-3-small).
        api_key: OpenAI API key; falls back to OPENAI_API_KEY env var.

    Returns:
        List of floats representing the embedding vector.
    """
    key = api_key or os.environ.get("OPENAI_API_KEY", "")
    if not key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = openai.OpenAI(api_key=key)

    response = client.embeddings.create(
        input=text,
        model=model,
    )

    return response.data[0].embedding


def embed_segments(
    texts: list[str],
    model: str = MODEL_ID,
    api_key: Optional[str] = None,
) -> list[list[float]]:
    """Embed multiple translated segments in a single API call.

    Args:
        texts: List of text segments to embed.
        model: OpenAI embedding model (default: text-embedding-3-small).
        api_key: OpenAI API key.

    Returns:
        List of embedding vectors, one per input segment.
    """
    key = api_key or os.environ.get("OPENAI_API_KEY", "")
    if not key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = openai.OpenAI(api_key=key)

    response = client.embeddings.create(
        input=texts,
        model=model,
    )

    return [item.embedding for item in response.data]


def build_translation_memory_index(
    segments: list[str],
    model: str = MODEL_ID,
    api_key: Optional[str] = None,
) -> dict:
    """Build a simple translation memory index with source text and embeddings.

    Args:
        segments: List of translated text segments to index.
        model: Embedding model identifier.
        api_key: OpenAI API key.

    Returns:
        Dict mapping index positions to {text, embedding} for TM search.
    """
    embeddings = embed_segments(segments, model=model, api_key=api_key)
    return {
        i: {"text": segments[i], "embedding": embeddings[i]}
        for i in range(len(segments))
    }


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two embedding vectors."""
    import math

    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def search_translation_memory(
    query: str,
    memory_index: dict,
    top_k: int = 5,
    model: str = MODEL_ID,
    api_key: Optional[str] = None,
) -> list[dict]:
    """Search the translation memory index for similar segments.

    Args:
        query: Query text to search for.
        memory_index: Index built by build_translation_memory_index.
        top_k: Number of results to return.
        model: Embedding model.
        api_key: OpenAI API key.

    Returns:
        List of {text, score} sorted by similarity descending.
    """
    query_embedding = embed_segment(query, model=model, api_key=api_key)

    scored = []
    for idx, entry in memory_index.items():
        score = cosine_similarity(query_embedding, entry["embedding"])
        scored.append({"text": entry["text"], "score": score})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]
