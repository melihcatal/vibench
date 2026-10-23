"""
translation_memory_embedding.py - Embed translated segments for translation-memory search.

Uses OpenAI Embeddings API (openai SDK) for generating embeddings.
Provider: OpenAI (api.openai.com)
Model: text-embedding-ada-002
"""

from typing import List, Dict, Any, Optional
import os

import openai
from translation_models import TranslationResponse


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_EMBEDDING_MODEL = "text-embedding-ada-002"


def get_openai_client() -> openai.OpenAI:
    """
    Get or create an OpenAI client for embedding operations.

    Connects to api.openai.com for text-embedding-ada-002 model access.

    Returns:
        Configured openai.OpenAI client instance.

    Raises:
        ValueError: If OPENAI_API_KEY is not set.
    """
    if not OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY environment variable is required "
            "for OpenAI Embeddings API access (api.openai.com)."
        )
    return openai.OpenAI(api_key=OPENAI_API_KEY)


def embed_text(text: str, model: str = OPENAI_EMBEDDING_MODEL) -> List[float]:
    """
    Embed a single text string using OpenAI's text-embedding-ada-002 model.

    Args:
        text: Text to embed.
        model: OpenAI embedding model identifier (default: text-embedding-ada-002).

    Returns:
        List of floats representing the embedding vector.
    """
    client = get_openai_client()
    response = client.embeddings.create(
        model=model,
        input=text,
    )
    return response.data[0].embedding


def embed_translation_segments(
    translations: List[Dict[str, str]],
    model: str = OPENAI_EMBEDDING_MODEL,
) -> List[Dict[str, Any]]:
    """
    Embed translated segments for translation-memory search.

    Creates embeddings for both source and translated text to enable
    similarity-based retrieval from translation memory.

    Args:
        translations: List of dicts with 'source' and 'target' keys.
        model: OpenAI embedding model identifier (default: text-embedding-ada-002).

    Returns:
        List of dicts with source, target, and their embeddings.
    """
    client = get_openai_client()

    source_texts = [t["source"] for t in translations]
    target_texts = [t["target"] for t in translations]

    source_response = client.embeddings.create(
        model=model,
        input=source_texts,
    )
    target_response = client.embeddings.create(
        model=model,
        input=target_texts,
    )

    results = []
    for i, (src, tgt) in enumerate(translations):
        results.append({
            "source": src,
            "target": tgt,
            "source_embedding": source_response.data[i].embedding,
            "target_embedding": target_response.data[i].embedding,
            "model": model,
            "provider": "openai",
            "endpoint": "api.openai.com",
        })

    return results


def search_translation_memory(
    query: str,
    memory: List[Dict[str, Any]],
    top_k: int = 5,
    model: str = OPENAI_EMBEDDING_MODEL,
) -> List[Dict[str, Any]]:
    """
    Search translation memory using embedding similarity.

    Uses OpenAI's text-embedding-ada-002 model to embed the query and
    find most similar segments in the translation memory.

    Args:
        query: Query text to search for.
        memory: List of embedded translation segments from embed_translation_segments.
        top_k: Number of top results to return.
        model: OpenAI embedding model identifier.

    Returns:
        List of top-k matching segments with similarity scores.
    """
    query_embedding = embed_text(query, model=model)

    results = []
    for segment in memory:
        similarity = _cosine_similarity(query_embedding, segment["source_embedding"])
        results.append({
            "source": segment["source"],
            "target": segment["target"],
            "similarity": similarity,
            "model": model,
            "provider": "openai",
        })

    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results[:top_k]


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    """Compute cosine similarity between two vectors."""
    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


if __name__ == "__main__":
    translations = [
        {"source": "Hello", "target": "Hola"},
        {"source": "Goodbye", "target": "Adiós"},
    ]
    memory = embed_translation_segments(translations)
    results = search_translation_memory("Hello there", memory)
    print(results)
