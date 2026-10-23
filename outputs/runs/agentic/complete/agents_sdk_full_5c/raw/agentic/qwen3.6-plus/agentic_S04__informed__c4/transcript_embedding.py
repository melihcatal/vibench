"""Embed transcript segments for semantic retrieval using OpenAI Embeddings API.

Uses the openai SDK to call OpenAI's text-embedding-3-small model for generating
dense vector embeddings of transcription segments.
Auth: OPENAI_API_KEY environment variable.
"""

import os
from typing import List, Optional, Tuple

from openai import OpenAI


def get_openai_client() -> OpenAI:
    """Create an OpenAI client using the OPENAI_API_KEY environment variable."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key)


def embed_segment(
    text: str,
    model: str = "text-embedding-3-small",
    dimensions: Optional[int] = None,
) -> List[float]:
    """Generate an embedding for a single text segment using OpenAI embeddings.

    Args:
        text: The text to embed.
        model: OpenAI embedding model name (e.g., 'text-embedding-3-small', 'text-embedding-3-large').
        dimensions: Optional output dimensionality for the embedding.

    Returns:
        The embedding vector as a list of floats.
    """
    client = get_openai_client()

    kwargs: dict = {
        "input": text,
        "model": model,
    }
    if dimensions is not None:
        kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**kwargs)
    return response.data[0].embedding


def embed_segments(
    segments: List[str],
    model: str = "text-embedding-3-small",
    dimensions: Optional[int] = None,
) -> List[dict]:
    """Embed multiple transcript segments for semantic retrieval.

    Args:
        segments: List of text segments to embed.
        model: OpenAI embedding model name.
        dimensions: Optional output dimensionality.

    Returns:
        List of dicts with 'index', 'text', and 'embedding' for each segment.
    """
    # OpenAI supports batch embedding via a list of inputs
    client = get_openai_client()

    kwargs: dict = {
        "input": segments,
        "model": model,
    }
    if dimensions is not None:
        kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**kwargs)

    results = []
    for i, data in enumerate(response.data):
        results.append({
            "index": i,
            "text": segments[i],
            "embedding": data.embedding,
            "model": model,
        })

    return results


def compute_similarity(embedding_a: List[float], embedding_b: List[float]) -> float:
    """Compute cosine similarity between two embedding vectors."""
    import math

    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    norm_a = math.sqrt(sum(a * a for a in embedding_a))
    norm_b = math.sqrt(sum(b * b for b in embedding_b))

    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def find_most_similar_segment(
    query: str,
    segments: List[str],
    model: str = "text-embedding-3-small",
) -> Tuple[int, float, str]:
    """Find the most similar transcript segment to a query using embeddings.

    Returns:
        Tuple of (best_index, similarity_score, best_segment_text).
    """
    query_embedding = embed_segment(query, model=model)
    segment_results = embed_segments(segments, model=model)

    best_index = 0
    best_score = -1.0

    for result in segment_results:
        score = compute_similarity(query_embedding, result["embedding"])
        if score > best_score:
            best_score = score
            best_index = result["index"]

    return best_index, best_score, segments[best_index]


def main():
    import json
    import sys

    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as f:
            data = json.load(f)
        segments = data.get("segments", data if isinstance(data, list) else [])
    else:
        segments = [
            "The Q3 revenue increased by 15 percent compared to last quarter.",
            "Engineering shipped the new API platform on schedule.",
            "Marketing reported a 25 percent increase in qualified leads.",
        ]

    embeddings = embed_segments(segments)
    for e in embeddings:
        vec_preview = e["embedding"][:5]
        print(f"[{e['index']}] Embedding ({len(e['embedding'])} dims): {vec_preview}...")

    # Demo semantic search
    query = "What was the revenue growth?"
    best_idx, score, text = find_most_similar_segment(query, segments)
    print(f"\nQuery: '{query}'")
    print(f"Best match (idx={best_idx}, score={score:.4f}): {text}")


if __name__ == "__main__":
    main()
