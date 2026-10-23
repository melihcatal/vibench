"""
Embed model outputs for clustering or retrieval using OpenAI Embeddings API.

Uses OpenAI platform API at api.openai.com with concrete model text-embedding-3-small
for generating vector embeddings of text outputs.
"""

import os
from typing import Any, Dict, List, Optional, Tuple

from openai import OpenAI


_OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
_OPENAI_EMBEDDING_DIMENSIONS = 1536


def get_openai_client() -> OpenAI:
    """Create OpenAI client for embeddings API access."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required.")
    return OpenAI(api_key=api_key, base_url="https://api.openai.com/v1")


def embed_text(
    text: str,
    model: str = _OPENAI_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
) -> Dict[str, Any]:
    """Generate embedding vector for a single text using OpenAI's text-embedding-3-small.

    Args:
        text: The text to embed.
        model: OpenAI embedding model identifier (text-embedding-3-small).
        dimensions: Optional output dimension count for text-embedding-3 models.

    Returns:
        Dict with 'vector' (list of floats) and 'usage' info.
    """
    client = get_openai_client()

    params: Dict[str, Any] = {
        "input": text,
        "model": model,
    }
    if dimensions is not None:
        params["dimensions"] = dimensions

    response = client.embeddings.create(**params)

    return {
        "vector": response.data[0].embedding,
        "usage_tokens": response.usage.total_tokens,
        "model": response.model,
    }


def embed_texts_batch(
    texts: List[str],
    model: str = _OPENAI_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
    batch_size: int = 100,
) -> List[Dict[str, Any]]:
    """Batch embed multiple texts using OpenAI's text-embedding-3-small.

    Args:
        texts: List of texts to embed.
        model: OpenAI embedding model identifier.
        dimensions: Optional output dimension count.
        batch_size: Max texts per API call (OpenAI limit is typically 100).

    Returns:
        List of dicts with vectors and usage for each input text.
    """
    client = get_openai_client()
    all_results = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]

        params: Dict[str, Any] = {
            "input": batch,
            "model": model,
        }
        if dimensions is not None:
            params["dimensions"] = dimensions

        response = client.embeddings.create(**params)

        for j, data in enumerate(response.data):
            all_results.append({
                "index": i + j,
                "vector": data.embedding,
                "usage_tokens": response.usage.total_tokens,
                "model": response.model,
            })

    return all_results


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Compute cosine similarity between two embedding vectors.

    Args:
        vec_a: First vector.
        vec_b: Second vector.

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


def find_most_similar(
    query_text: str,
    candidate_texts: List[str],
    top_k: int = 5,
    model: str = _OPENAI_EMBEDDING_MODEL,
) -> List[Tuple[str, float, int]]:
    """Find the most similar texts to a query using OpenAI embeddings.

    Args:
        query_text: The query text.
        candidate_texts: List of candidate texts to search.
        top_k: Number of top results to return.
        model: OpenAI embedding model identifier.

    Returns:
        List of (text, similarity_score, original_index) tuples.
    """
    query_result = embed_text(query_text, model=model)
    query_vector = query_result["vector"]

    candidate_results = embed_texts_batch(candidate_texts, model=model)

    scored = []
    for result in candidate_results:
        sim = cosine_similarity(query_vector, result["vector"])
        scored.append((candidate_texts[result["index"]], sim, result["index"]))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]


def get_embedding_dimensions(model: str = _OPENAI_EMBEDDING_MODEL) -> int:
    """Get the default embedding dimension for the model.

    Args:
        model: OpenAI embedding model identifier.

    Returns:
        Default dimension count for the model.
    """
    dimension_map = {
        "text-embedding-3-small": 1536,
        "text-embedding-3-large": 3072,
        "text-embedding-ada-002": 1536,
    }
    return dimension_map.get(model, 1536)


if __name__ == "__main__":
    texts = [
        "Machine learning models process data to find patterns.",
        "Deep learning uses neural networks with many layers.",
        "The weather is sunny and warm today.",
        "Python is a popular programming language for AI.",
    ]

    results = embed_texts_batch(texts, model="text-embedding-3-small")
    for r in results:
        print(f"Index {r['index']}: vector length = {len(r['vector'])}")

    similar = find_most_similar(
        "AI and data science programming",
        texts,
        top_k=3,
    )
    print("\nMost similar to 'AI and data science programming':")
    for text, score, idx in similar:
        print(f"  [{idx:.0%}] {text}")
