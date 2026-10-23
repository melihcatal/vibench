"""
[LATER-STEP] moderation_reason_embedding.py - Embed moderation rationales for case retrieval.

Uses the OpenAI Embeddings API (model: text-embedding-3-small) to generate
dense vector embeddings for moderation rationales, enabling semantic search
and similar-case retrieval.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from openai import OpenAI


_EMBEDDING_MODEL = "text-embedding-3-small"
_EMBEDDING_DIMENSION = 1536


def embed_moderation_reason(
    reason_text: str,
    api_key: Optional[str] = None,
    model: str = _EMBEDDING_MODEL,
    dimensions: int = _EMBEDDING_DIMENSION,
) -> List[float]:
    """
    Generate an embedding for a single moderation rationale.

    Parameters
    ----------
    reason_text : str
        The moderation rationale text to embed.
    api_key : str, optional
        OpenAI API key. Falls back to OPENAI_API_KEY env var.
    model : str
        OpenAI embedding model to use (default: text-embedding-3-small).
    dimensions : int
        Desired embedding dimensions (max 1536 for text-embedding-3-small).

    Returns
    -------
    list[float]
        The embedding vector.
    """
    if not reason_text or not reason_text.strip():
        return [0.0] * dimensions

    api_key = api_key or __import__("os").environ.get("OPENAI_API_KEY", "")
    client = OpenAI(api_key=api_key)

    try:
        response = client.embeddings.create(
            model=model,
            input=reason_text,
            dimensions=dimensions,
        )
        return response.data[0].embedding
    finally:
        if hasattr(client, "close"):
            client.close()


def embed_reasons_batch(
    reason_texts: List[str],
    api_key: Optional[str] = None,
    model: str = _EMBEDDING_MODEL,
    dimensions: int = _EMBEDDING_DIMENSION,
) -> List[Dict[str, Any]]:
    """
    Embed multiple moderation rationales in batch.

    Returns a list of dicts, each containing the original text, its embedding,
    and metadata.
    """
    api_key = api_key or __import__("os").environ.get("OPENAI_API_KEY", "")
    client = OpenAI(api_key=api_key)

    results: List[Dict[str, Any]] = []
    # OpenAI embeddings API can handle up to 2048 tokens per batch
    # Process in chunks of 100 to stay within API limits
    chunk_size = 100
    for i in range(0, len(reason_texts), chunk_size):
        chunk = reason_texts[i : i + chunk_size]
        try:
            response = client.embeddings.create(
                model=model,
                input=chunk,
                dimensions=dimensions,
            )
            for item in response.data:
                results.append(
                    {
                        "text": chunk[item.index],
                        "embedding": item.embedding,
                        "index": i + item.index,
                        "model": model,
                    }
                )
        finally:
            pass

    if hasattr(client, "close"):
        client.close()

    return results


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Compute cosine similarity between two embedding vectors."""
    import math

    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def find_similar_cases(
    query_reason: str,
    case_reasons: List[Dict[str, Any]],
    api_key: Optional[str] = None,
    top_k: int = 5,
) -> List[Dict[str, Any]]:
    """
    Find the most similar prior moderation cases to a new rationale.

    Parameters
    ----------
    query_reason : str
        The new moderation rationale to search for similar cases.
    case_reasons : list[dict]
        List of dicts, each with 'text' and 'embedding' keys.
    api_key : str, optional
        OpenAI API key.
    top_k : int
        Number of similar cases to return.

    Returns
    -------
    list[dict]
        The top-k most similar cases, each with a 'similarity' score added.
    """
    query_embedding = embed_moderation_reason(query_reason, api_key)

    scored_cases = []
    for case in case_reasons:
        if "embedding" not in case:
            continue
        similarity = cosine_similarity(query_embedding, case["embedding"])
        scored_cases.append({**case, "similarity": round(similarity, 4)})

    scored_cases.sort(key=lambda c: c["similarity"], reverse=True)
    return scored_cases[:top_k]


def main() -> None:
    import sys
    if len(sys.argv) < 2:
        print("Usage: python moderation_reason_embedding.py <reason_text>")
        sys.exit(1)
    text = " ".join(sys.argv[1:])
    embedding = embed_moderation_reason(text)
    print(f"Model: {_EMBEDDING_MODEL}")
    print(f"Dimensions: {len(embedding)}")
    print(f"Embedding (first 5): {embedding[:5]}")


if __name__ == "__main__":
    main()
