"""Embed narration scripts for voice-asset search using Cohere Embed API."""

from typing import List, Optional

import cohere


def embed_script(
    text: str,
    model: str = "embed-english-v3.0",
    input_type: str = "search_document",
) -> List[float]:
    """Embed a narration script using Cohere's embed endpoint.

    Uses the cohere.Client connecting to api.cohere.ai to generate vector
    embeddings for the given text. The embedding can be used for voice-asset
    search, similarity matching, or archival retrieval.
    """
    client = cohere.Client()

    response = client.embed(
        texts=[text],
        model=model,
        input_type=input_type,
    )

    embeddings = response.embeddings
    if not embeddings:
        raise ValueError("Cohere API returned empty embeddings")
    return embeddings[0]


def embed_scripts_batch(
    texts: List[str],
    model: str = "embed-english-v3.0",
    input_type: str = "search_document",
    truncate: str = "END",
) -> List[List[float]]:
    """Embed multiple narration scripts in a batch via Cohere's embed endpoint.

    Connects to api.cohere.ai to generate embeddings for a list of text segments.
    Returns a list of embedding vectors, one per input text.
    """
    client = cohere.Client()

    response = client.embed(
        texts=texts,
        model=model,
        input_type=input_type,
        truncate=truncate,
    )

    return response.embeddings


def search_voice_assets(
    query: str,
    asset_embeddings: List[List[float]],
    asset_ids: List[str],
    top_k: int = 5,
    model: str = "embed-english-v3.0",
) -> List[dict]:
    """Search voice assets by embedding a query and finding the nearest matches.

    Uses cohere.Client to embed the query text via api.cohere.ai, then computes
    cosine similarity against pre-computed asset embeddings to find the most
    relevant voice assets.
    """
    client = cohere.Client()

    query_embedding_response = client.embed(
        texts=[query],
        model=model,
        input_type="search_query",
    )
    query_vector = query_embedding_response.embeddings[0]

    similarities = []
    for i, asset_vec in enumerate(asset_embeddings):
        sim = _cosine_similarity(query_vector, asset_vec)
        similarities.append((i, sim))

    similarities.sort(key=lambda x: x[1], reverse=True)
    results = []
    for idx, sim in similarities[:top_k]:
        results.append({
            "asset_id": asset_ids[idx],
            "similarity": sim,
            "rank": idx,
        })
    return results


def _cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Compute cosine similarity between two vectors."""
    import math
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)
