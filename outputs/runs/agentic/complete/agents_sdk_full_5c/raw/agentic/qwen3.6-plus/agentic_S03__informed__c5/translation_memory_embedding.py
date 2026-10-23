"""
translation_memory_embedding.py - Embed translated segments for translation-memory search using OpenAI Embeddings API.

Provider: OpenAI Embeddings API
SDK: openai
Auth: OPENAI_API_KEY environment variable
Model: text-embedding-3-small
"""

import os
from typing import Dict, List, Optional, Tuple

from openai import OpenAI


def _chunk_texts(
    texts: List[str],
    batch_size: int = 100,
) -> List[List[str]]:
    """Split texts into batches for embedding API calls."""
    return [texts[i : i + batch_size] for i in range(0, len(texts), batch_size)]


def embed_translation_segments(
    source_texts: List[str],
    translated_texts: List[str],
    model: str = "text-embedding-3-small",
    batch_size: int = 100,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
) -> Dict:
    """
    Embed translated segments for translation-memory (TM) search using
    OpenAI's text-embedding-3-small model.

    Generates embeddings for both source and translated texts, pairing them
    so that a translation memory system can find similar segments for reuse.

    Args:
        source_texts: List of original source language text segments.
        translated_texts: List of corresponding translated text segments.
        model: OpenAI embedding model. Defaults to 'text-embedding-3-small'.
        batch_size: Number of texts to embed per API call (max 100 for OpenAI).
            Defaults to 100.
        dimensions: Optional output dimension count (e.g., 256 or 512 to reduce
            storage). If None, uses the model's default dimension size.
        api_key: OpenAI API key. If None, reads from OPENAI_API_KEY env variable.

    Returns:
        Dict with embedding results:
        {
            "segments": [
                {
                    "index": int,
                    "source_text": str,
                    "translated_text": str,
                    "source_embedding": List[float],
                    "translation_embedding": List[float],
                },
                ...
            ],
            "model": str,
            "total_segments": int,
            "embedding_dimensions": int,
        }

    Raises:
        ValueError: If source_texts and translated_texts lengths don't match.
        openai.OpenAIError: If the OpenAI API request fails.
    """
    if len(source_texts) != len(translated_texts):
        raise ValueError(
            "source_texts and translated_texts must have the same length."
        )

    openai_key = api_key or os.environ.get("OPENAI_API_KEY", "")
    if not openai_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable or api_key parameter "
            "is required for OpenAI Embeddings API."
        )

    client = OpenAI(api_key=openai_key)

    embed_kwargs: Dict = {"model": model}
    if dimensions is not None:
        embed_kwargs["dimensions"] = dimensions

    segments = []
    actual_dimensions = 0

    for source_batch, translation_batch in zip(
        _chunk_texts(source_texts, batch_size),
        _chunk_texts(translated_texts, batch_size),
    ):
        # Embed source texts
        source_response = client.embeddings.create(
            input=source_batch,
            **embed_kwargs,
        )
        # Embed translated texts
        translation_response = client.embeddings.create(
            input=translation_batch,
            **embed_kwargs,
        )

        start_index = len(segments)
        for i, (src, tgt) in enumerate(zip(source_batch, translation_batch)):
            source_embedding = source_response.data[i].embedding
            translation_embedding = translation_response.data[i].embedding

            if start_index + i == 0 and not actual_dimensions:
                actual_dimensions = len(source_embedding)

            segments.append({
                "index": start_index + i,
                "source_text": src,
                "translated_text": tgt,
                "source_embedding": source_embedding,
                "translation_embedding": translation_embedding,
            })

    return {
        "segments": segments,
        "model": model,
        "total_segments": len(segments),
        "embedding_dimensions": actual_dimensions,
    }


def search_translation_memory(
    query_text: str,
    tm_segments: Dict,
    top_k: int = 5,
    use_source: bool = True,
) -> List[Dict]:
    """
    Search the translation memory for segments similar to the query text
    using cosine similarity over precomputed OpenAI embeddings.

    Args:
        query_text: The text to search for similar segments.
        tm_segments: The translation memory dict returned by embed_translation_segments.
        top_k: Number of most similar segments to return.
        use_source: If True, compare against source text embeddings.
            If False, compare against translation embeddings.

    Returns:
        List of top_k most similar segments with similarity scores, sorted
        from most to least similar.
    """
    if not tm_segments.get("segments"):
        return []

    openai_key = os.environ.get("OPENAI_API_KEY", "")
    client = OpenAI(api_key=openai_key)

    model = tm_segments.get("model", "text-embedding-3-small")
    query_response = client.embeddings.create(
        input=[query_text],
        model=model,
    )
    query_embedding = query_response.data[0].embedding

    scored_results = []
    for segment in tm_segments["segments"]:
        if use_source:
            segment_embedding = segment["source_embedding"]
        else:
            segment_embedding = segment["translation_embedding"]

        similarity = _cosine_similarity(query_embedding, segment_embedding)

        scored_results.append({
            "index": segment["index"],
            "source_text": segment["source_text"],
            "translated_text": segment["translated_text"],
            "similarity_score": similarity,
        })

    scored_results.sort(key=lambda x: x["similarity_score"], reverse=True)
    return scored_results[:top_k]


def _cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Compute cosine similarity between two vectors."""
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = sum(a * a for a in vec_a) ** 0.5
    norm_b = sum(b * b for b in vec_b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)
