"""Embed narration scripts for voice-asset search using OpenAI Embeddings API."""

import os
from typing import List, Optional

from openai import OpenAI


def embed_script(
    text: str,
    model: str = "text-embedding-3-small",
    api_key: Optional[str] = None,
    dimensions: Optional[int] = None,
) -> List[float]:
    """Generate an embedding vector for a narration script using OpenAI Embeddings.

    Uses the OpenAI text-embedding-3-small or text-embedding-3-large model.
    Requires OPENAI_API_KEY environment variable if api_key is not provided.

    Args:
        text: The narration script text to embed.
        model: OpenAI embedding model ID. Defaults to "text-embedding-3-small".
        api_key: OpenAI API key. Falls back to OPENAI_API_KEY env var.
        dimensions: Optional output dimensionality (supported by v3 models).

    Returns:
        List of floats representing the embedding vector.
    """
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OpenAI API key required. Set OPENAI_API_KEY or pass api_key.")

    client = OpenAI(api_key=key)

    embed_kwargs: dict = {
        "input": text,
        "model": model,
    }
    if dimensions is not None:
        embed_kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**embed_kwargs)

    return response.data[0].embedding


def embed_scripts_batch(
    texts: List[str],
    model: str = "text-embedding-3-small",
    api_key: Optional[str] = None,
    dimensions: Optional[int] = None,
) -> List[List[float]]:
    """Generate embeddings for a batch of narration scripts via OpenAI.

    Args:
        texts: List of script strings to embed.
        model: OpenAI embedding model ID.
        api_key: OpenAI API key.
        dimensions: Optional output dimensionality.

    Returns:
        List of embedding vectors, one per input text.
    """
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OpenAI API key required. Set OPENAI_API_KEY or pass api_key.")

    client = OpenAI(api_key=key)

    embed_kwargs: dict = {
        "input": texts,
        "model": model,
    }
    if dimensions is not None:
        embed_kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**embed_kwargs)

    return [item.embedding for item in response.data]


def cosine_similarity(
    vec_a: List[float],
    vec_b: List[float],
) -> float:
    """Compute cosine similarity between two embedding vectors.

    Args:
        vec_a: First embedding vector.
        vec_b: Second embedding vector.

    Returns:
        Cosine similarity score between 0 and 1.
    """
    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must have the same dimensionality.")

    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = sum(a * a for a in vec_a) ** 0.5
    norm_b = sum(b * b for b in vec_b) ** 0.5

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


def search_voice_assets(
    query_text: str,
    asset_texts: List[str],
    asset_ids: Optional[List[str]] = None,
    model: str = "text-embedding-3-small",
    api_key: Optional[str] = None,
    top_k: int = 5,
) -> List[dict]:
    """Search for the most relevant voice assets using OpenAI embeddings.

    Embeds the query and all candidate asset texts, then ranks by cosine similarity.

    Args:
        query_text: The search query script.
        asset_texts: List of asset description texts to search against.
        asset_ids: Optional list of asset IDs (defaults to indices).
        model: OpenAI embedding model ID.
        api_key: OpenAI API key.
        top_k: Number of top results to return.

    Returns:
        Ranked list of dicts with 'id', 'score', and 'text'.
    """
    query_embedding = embed_script(query_text, model=model, api_key=api_key)
    asset_embeddings = embed_scripts_batch(
        asset_texts, model=model, api_key=api_key
    )

    results = []
    ids = asset_ids or [str(i) for i in range(len(asset_texts))]

    for idx, asset_emb in enumerate(asset_embeddings):
        score = cosine_similarity(query_embedding, asset_emb)
        results.append({
            "id": ids[idx],
            "score": score,
            "text": asset_texts[idx],
        })

    results.sort(key=lambda r: r["score"], reverse=True)
    return results[:top_k]
