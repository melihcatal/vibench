"""Embed translated segments for translation-memory search using OpenAI Embeddings API.

Generates vector embeddings for translated text segments so they can be
stored and searched in a translation-memory system for reuse and consistency.
"""

import os
from typing import Any

from openai import OpenAI

EMBEDDING_MODEL = "text-embedding-3-small"


def embed_translation_segment(
    segment_text: str,
    source_lang: str = "en",
    target_lang: str = "es",
    model: str = EMBEDDING_MODEL,
) -> dict[str, Any]:
    """Generate an embedding for a translated text segment using OpenAI.

    Args:
        segment_text: The translated text segment to embed.
        source_lang: Source language code for metadata.
        target_lang: Target language code for metadata.
        model: OpenAI embedding model identifier.

    Returns:
        Dictionary containing the embedding vector and metadata.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required for OpenAI Embeddings API")

    client = OpenAI(api_key=api_key)

    response = client.embeddings.create(
        input=segment_text,
        model=model,
        dimensions=1536,
    )

    embedding_data = response.data[0]

    return {
        "text": segment_text,
        "source_lang": source_lang,
        "target_lang": target_lang,
        "embedding": embedding_data.embedding,
        "model": model,
        "provider": "openai",
        "usage_tokens": response.usage.total_tokens,
    }


def embed_translation_batch(
    segments: list[str],
    source_lang: str = "en",
    target_lang: str = "es",
    model: str = EMBEDDING_MODEL,
    batch_size: int = 100,
) -> list[dict[str, Any]]:
    """Generate embeddings for multiple translated segments using OpenAI.

    Args:
        segments: List of translated text segments to embed.
        source_lang: Source language code for metadata.
        target_lang: Target language code for metadata.
        model: OpenAI embedding model identifier.
        batch_size: Maximum segments per API call (OpenAI allows up to 2048 tokens per batch).

    Returns:
        List of embedding result dictionaries corresponding to each input segment.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required for OpenAI Embeddings API")

    client = OpenAI(api_key=api_key)
    all_results: list[dict[str, Any]] = []

    for i in range(0, len(segments), batch_size):
        batch = segments[i : i + batch_size]

        response = client.embeddings.create(
            input=batch,
            model=model,
            dimensions=1536,
        )

        for idx, embedding_data in enumerate(response.data):
            all_results.append({
                "text": batch[idx],
                "source_lang": source_lang,
                "target_lang": target_lang,
                "embedding": embedding_data.embedding,
                "model": model,
                "provider": "openai",
                "usage_tokens": response.usage.total_tokens,
            })

    return all_results


def similarity_search(
    query_embedding: list[float],
    stored_segments: list[dict[str, Any]],
    top_k: int = 5,
) -> list[dict[str, Any]]:
    """Find the most similar stored translation segments to a query embedding.

    Uses cosine similarity to rank stored segments by relevance.

    Args:
        query_embedding: The embedding vector of the query text.
        stored_segments: List of previously stored segment embedding dicts.
        top_k: Number of top results to return.

    Returns:
        Top-K most similar segments with similarity scores.
    """
    import math

    def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot_product / (norm_a * norm_b)

    scored = []
    for segment in stored_segments:
        score = cosine_similarity(query_embedding, segment["embedding"])
        scored.append({**segment, "similarity_score": score})

    scored.sort(key=lambda x: x["similarity_score"], reverse=True)
    return scored[:top_k]
