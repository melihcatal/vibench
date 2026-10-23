"""
Embed narration scripts for voice-asset search using OpenAI Embeddings.

Provider: OpenAI Embeddings
SDK: openai
Auth: OPENAI_API_KEY
"""

import os
from typing import Optional, List, Dict, Any

import openai

OPENAI_API_KEY_ENV = "OPENAI_API_KEY"

# OpenAI embedding model identifiers
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
LARGE_EMBEDDING_MODEL = "text-embedding-3-large"
ADA_EMBEDDING_MODEL = "text-embedding-ada-002"


def get_openai_client(api_key: Optional[str] = None) -> openai.OpenAI:
    """Create an OpenAI client for embeddings.

    Args:
        api_key: OpenAI API key. Falls back to OPENAI_API_KEY env var.

    Returns:
        Initialized openai.OpenAI client.
    """
    key = api_key or os.environ.get(OPENAI_API_KEY_ENV)
    if not key:
        raise ValueError(
            f"OpenAI API key not provided. Set {OPENAI_API_KEY_ENV}."
        )
    return openai.OpenAI(api_key=key)


def embed_script(
    text: str,
    model: str = DEFAULT_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    dimensions: Optional[int] = None,
) -> List[float]:
    """Generate embedding vector for a narration script using OpenAI.

    Args:
        text: Narration script text.
        model: OpenAI embedding model (e.g. text-embedding-3-small).
        api_key: OpenAI API key.
        dimensions: Optional output dimensionality (for text-embedding-3 models).

    Returns:
        Embedding vector as list of floats.
    """
    client = get_openai_client(api_key)

    kwargs: Dict[str, Any] = {
        "input": text,
        "model": model,
    }

    if dimensions is not None:
        kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**kwargs)
    return response.data[0].embedding


def embed_scripts_batch(
    texts: List[str],
    model: str = DEFAULT_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    dimensions: Optional[int] = None,
) -> List[List[float]]:
    """Batch generate embeddings for multiple narration scripts.

    Args:
        texts: List of narration script texts.
        model: OpenAI embedding model (e.g. text-embedding-3-small).
        api_key: OpenAI API key.
        dimensions: Optional output dimensionality.

    Returns:
        List of embedding vectors.
    """
    client = get_openai_client(api_key)

    kwargs: Dict[str, Any] = {
        "input": texts,
        "model": model,
    }

    if dimensions is not None:
        kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**kwargs)
    return [item.embedding for item in response.data]


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Compute cosine similarity between two embedding vectors.

    Args:
        vec_a: First embedding vector.
        vec_b: Second embedding vector.

    Returns:
        Cosine similarity score (0.0 to 1.0).
    """
    import math

    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot / (norm_a * norm_b)


def search_similar_scripts(
    query_text: str,
    script_embeddings: Dict[str, List[float]],
    model: str = DEFAULT_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    top_k: int = 5,
    threshold: float = 0.0,
) -> List[Dict[str, Any]]:
    """Search for similar narration scripts using embeddings.

    Args:
        query_text: Query narration script.
        script_embeddings: Dict mapping script IDs to embedding vectors.
        model: OpenAI embedding model.
        api_key: OpenAI API key.
        top_k: Number of top results to return.
        threshold: Minimum similarity score.

    Returns:
        List of dicts with script_id and similarity score, sorted by score.
    """
    query_embedding = embed_script(query_text, model=model, api_key=api_key)

    scored = []
    for script_id, embedding in script_embeddings.items():
        sim = cosine_similarity(query_embedding, embedding)
        if sim >= threshold:
            scored.append({"script_id": script_id, "similarity": sim})

    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return scored[:top_k]


def get_embedding_metadata(
    model: str = DEFAULT_EMBEDDING_MODEL,
) -> Dict[str, Any]:
    """Get metadata about the embedding model.

    Args:
        model: OpenAI embedding model identifier.

    Returns:
        Dict with model metadata.
    """
    model_info = {
        "text-embedding-3-small": {
            "dimensions": 1536,
            "max_input_tokens": 8191,
            "performance": "high",
        },
        "text-embedding-3-large": {
            "dimensions": 3072,
            "max_input_tokens": 8191,
            "performance": "highest",
        },
        "text-embedding-ada-002": {
            "dimensions": 1536,
            "max_input_tokens": 8191,
            "performance": "standard",
        },
    }
    return model_info.get(model, {"dimensions": None, "max_input_tokens": None})
