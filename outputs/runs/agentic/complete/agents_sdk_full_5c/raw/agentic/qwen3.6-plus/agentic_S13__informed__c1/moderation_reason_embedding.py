"""
[LATER-STEP] moderation_reason_embedding.py - Embed moderation rationales
for case retrieval using OpenAI Embeddings API.

Provider: OpenAI
SDK: openai
Auth: OPENAI_API_KEY
"""

import os
from typing import Optional

from openai import OpenAI

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_moderation_reason(
    reason_text: str,
    model: str = OPENAI_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
) -> dict:
    """
    Generate an embedding vector for a moderation rationale using
    the OpenAI Embeddings API (text-embedding-3-small model).

    Args:
        reason_text: The moderation reason/rationale text to embed.
        model: OpenAI embedding model identifier.
        api_key: Optional OpenAI API key override.

    Returns:
        Dict with 'embedding' (list of floats), 'model', 'text'.
    """
    key = api_key or os.environ.get("OPENAI_API_KEY", "")
    client = OpenAI(api_key=key)

    response = client.embeddings.create(
        model=model,
        input=reason_text,
    )

    embedding = response.data[0].embedding

    return {
        "text": reason_text,
        "embedding": embedding,
        "model": model,
        "dimension": len(embedding),
    }


def embed_moderation_reasons_batch(
    reasons: list[str],
    model: str = OPENAI_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
) -> list[dict]:
    """
    Generate embeddings for multiple moderation rationales in a single
    OpenAI API call.

    Args:
        reasons: List of rationale texts to embed.
        model: OpenAI embedding model identifier.
        api_key: Optional OpenAI API key override.

    Returns:
        List of dicts with embedding results for each rationale.
    """
    key = api_key or os.environ.get("OPENAI_API_KEY", "")
    client = OpenAI(api_key=key)

    response = client.embeddings.create(
        model=model,
        input=reasons,
    )

    results = []
    for item in response.data:
        results.append({
            "text": reasons[item.index],
            "embedding": item.embedding,
            "model": model,
            "dimension": len(item.embedding),
        })

    return results


def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """Compute cosine similarity between two embedding vectors."""
    import math
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def find_similar_cases(
    query_reason: str,
    stored_cases: list[dict],
    top_k: int = 5,
    model: str = OPENAI_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
) -> list[dict]:
    """
    Find the most similar stored moderation cases to a query reason.

    Args:
        query_reason: The query rationale text.
        stored_cases: List of dicts with 'text' and 'embedding' keys.
        top_k: Number of most similar cases to return.
        model: OpenAI embedding model identifier.
        api_key: Optional OpenAI API key override.

    Returns:
        List of stored cases sorted by similarity score, descending.
    """
    query_result = embed_moderation_reason(query_reason, model=model, api_key=api_key)
    query_embedding = query_result["embedding"]

    scored = []
    for case in stored_cases:
        sim = cosine_similarity(query_embedding, case["embedding"])
        scored.append({"similarity": sim, **case})

    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return scored[:top_k]


if __name__ == "__main__":
    sample_reason = "Content was blocked due to high violence severity score."
    result = embed_moderation_reason(sample_reason)
    print(f"Model: {result['model']}, Dimension: {result['dimension']}")
