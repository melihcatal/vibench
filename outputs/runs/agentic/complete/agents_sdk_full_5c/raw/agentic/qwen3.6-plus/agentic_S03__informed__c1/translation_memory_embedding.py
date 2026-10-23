"""
Embed translated segments for translation-memory search.

Provider: OpenAI Embeddings
SDK: openai
Auth: OPENAI_API_KEY
Model: text-embedding-3-small
"""

import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def embed_segments(
    segments: List[str],
    model: str = "text-embedding-3-small",
    dimensions: Optional[int] = None,
) -> List[List[float]]:
    """
    Embed translated text segments using OpenAI's text-embedding-3-small model.

    Args:
        segments: List of text segments to embed.
        model: OpenAI embedding model identifier (default: text-embedding-3-small).
        dimensions: Optional output dimensionality for the embeddings.

    Returns:
        List of embedding vectors (list of floats per segment).
    """
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required.")

    client = OpenAI(api_key=api_key)

    kwargs = {"model": model}
    if dimensions is not None:
        kwargs["dimensions"] = dimensions

    response = client.embeddings.create(input=segments, **kwargs)

    embeddings = []
    for data in sorted(response.data, key=lambda d: d.index):
        embeddings.append(data.embedding)

    return embeddings


def embed_translation_pair(
    source_text: str,
    translated_text: str,
    model: str = "text-embedding-3-small",
) -> Dict[str, Any]:
    """
    Embed both source and translated text for bilingual translation memory.

    Args:
        source_text: Original source text.
        translated_text: Translated target text.
        model: OpenAI embedding model identifier.

    Returns:
        Dictionary containing both embeddings and metadata.
    """
    embeddings = embed_segments([source_text, translated_text], model=model)
    return {
        "source_text": source_text,
        "translated_text": translated_text,
        "source_embedding": embeddings[0],
        "translated_embedding": embeddings[1],
        "model": model,
        "dimension": len(embeddings[0]),
    }


def build_translation_memory_index(
    segments: List[Dict[str, str]],
    model: str = "text-embedding-3-small",
) -> List[Dict[str, Any]]:
    """
    Build a translation-memory index from parallel source/translation pairs.

    Args:
        segments: List of dicts with 'source' and 'target' keys.
        model: OpenAI embedding model identifier.

    Returns:
        List of indexed translation memory entries with embeddings.
    """
    source_texts = [seg["source"] for seg in segments]
    target_texts = [seg["target"] for seg in segments]

    source_embeddings = embed_segments(source_texts, model=model)
    target_embeddings = embed_segments(target_texts, model=model)

    index = []
    for i, seg in enumerate(segments):
        index.append({
            "source_text": seg["source"],
            "target_text": seg["target"],
            "source_language": seg.get("source_language", "unknown"),
            "target_language": seg.get("target_language", "unknown"),
            "source_embedding": source_embeddings[i],
            "target_embedding": target_embeddings[i],
            "model": model,
        })

    return index


def find_similar_segments(
    query_embedding: List[float],
    memory_index: List[Dict[str, Any]],
    top_k: int = 5,
) -> List[Dict[str, Any]]:
    """
    Find the most similar segments in the translation memory index.

    Uses cosine similarity for comparison.

    Args:
        query_embedding: Embedding vector for the query segment.
        memory_index: List of indexed translation memory entries.
        top_k: Number of top matches to return.

    Returns:
        Top-k most similar segments with similarity scores.
    """
    import math

    def dot_product(a: List[float], b: List[float]) -> float:
        return sum(x * y for x, y in zip(a, b))

    def magnitude(a: List[float]) -> float:
        return math.sqrt(sum(x * x for x in a))

    scored = []
    for entry in memory_index:
        sim = dot_product(query_embedding, entry["source_embedding"]) / (
            magnitude(query_embedding) * magnitude(entry["source_embedding"]) + 1e-9
        )
        scored.append({**entry, "similarity": sim})

    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return scored[:top_k]


if __name__ == "__main__":
    segments = [
        {"source": "Hello world", "target": "Hola mundo", "source_language": "en", "target_language": "es"},
        {"source": "Good morning", "target": "Buenos días", "source_language": "en", "target_language": "es"},
    ]
    index = build_translation_memory_index(segments)
    print(f"Indexed {len(index)} translation pairs with model text-embedding-3-small")
