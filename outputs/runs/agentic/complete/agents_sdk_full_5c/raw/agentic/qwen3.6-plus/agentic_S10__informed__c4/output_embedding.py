"""
Embed model outputs for clustering or retrieval using OpenAI Embeddings API.
Provider: OpenAI (openai SDK, OPENAI_API_KEY)
"""

import os
from typing import List, Optional, Dict, Any

import openai


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-large"


def _get_openai_client() -> openai.OpenAI:
    """Create and return an authenticated OpenAI client."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return openai.OpenAI(api_key=api_key)


def embed_text(
    text: str,
    model: str = DEFAULT_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
) -> List[float]:
    """
    Generate an embedding vector for a single text using OpenAI Embeddings API.

    Args:
        text: The text to embed.
        model: OpenAI embedding model identifier.
        dimensions: Optional output dimensions (truncates vector if specified).

    Returns:
        List of floats representing the embedding vector.
    """
    client = _get_openai_client()

    kwargs: Dict[str, Any] = {
        "input": text,
        "model": model,
    }
    if dimensions is not None:
        kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**kwargs)
    return response.data[0].embedding


def embed_texts(
    texts: List[str],
    model: str = DEFAULT_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
) -> List[List[float]]:
    """
    Generate embedding vectors for multiple texts.

    Args:
        texts: List of texts to embed.
        model: OpenAI embedding model identifier.
        dimensions: Optional output dimensions.

    Returns:
        List of embedding vectors.
    """
    client = _get_openai_client()

    kwargs: Dict[str, Any] = {
        "input": texts,
        "model": model,
    }
    if dimensions is not None:
        kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**kwargs)
    return [item.embedding for item in response.data]


def embed_model_output(
    output_text: str,
    model: str = DEFAULT_EMBEDDING_MODEL,
) -> Dict[str, Any]:
    """
    Embed a model output and return metadata alongside the vector.

    Args:
        output_text: The model-generated text to embed.
        model: OpenAI embedding model identifier.

    Returns:
        Dict with embedding vector and metadata.
    """
    embedding = embed_text(output_text, model=model)
    return {
        "text": output_text,
        "embedding": embedding,
        "model": model,
        "dimensions": len(embedding),
    }


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """
    Compute cosine similarity between two embedding vectors.

    Args:
        vec_a: First embedding vector.
        vec_b: Second embedding vector.

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
