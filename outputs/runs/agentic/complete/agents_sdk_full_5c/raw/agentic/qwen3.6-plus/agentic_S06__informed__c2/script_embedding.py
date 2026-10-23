"""Embed narration scripts for voice-asset search using OpenAI Embeddings API."""

import os
from typing import Optional, List, Dict, Any
from openai import OpenAI

from speech_models import TTSRequest


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_script(
    text: str,
    model: str = OPENAI_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    dimensions: Optional[int] = None,
) -> List[float]:
    """Generate an embedding vector for a narration script using OpenAI Embeddings API.

    Args:
        text: The narration script text to embed.
        model: OpenAI embedding model ID (default: text-embedding-3-small).
        api_key: OpenAI API key (defaults to OPENAI_API_KEY env var).
        dimensions: Optional output dimensionality (e.g., 256, 512, 1024, 1536).

    Returns:
        List of floats representing the embedding vector.

    Raises:
        EnvironmentError: If OPENAI_API_KEY is not set.
    """
    if api_key is None:
        api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY environment variable is required. "
            "Set it to your OpenAI API key from https://platform.openai.com/"
        )

    client = OpenAI(api_key=api_key)

    params: Dict[str, Any] = {
        "input": text,
        "model": model,
    }
    if dimensions is not None:
        params["dimensions"] = dimensions

    response = client.embeddings.create(**params)
    return response.data[0].embedding


def embed_scripts_batch(
    texts: List[str],
    model: str = OPENAI_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    dimensions: Optional[int] = None,
) -> List[List[float]]:
    """Generate embeddings for multiple narration scripts in a single API call.

    Args:
        texts: List of narration script texts to embed.
        model: OpenAI embedding model ID.
        api_key: OpenAI API key.
        dimensions: Optional output dimensionality.

    Returns:
        List of embedding vectors, one per input text.
    """
    if api_key is None:
        api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY environment variable is required.")

    client = OpenAI(api_key=api_key)

    params: Dict[str, Any] = {
        "input": texts,
        "model": model,
    }
    if dimensions is not None:
        params["dimensions"] = dimensions

    response = client.embeddings.create(**params)
    return [item.embedding for item in response.data]


def embed_tts_request(
    request: TTSRequest,
    model: str = OPENAI_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Embed a TTS request for voice-asset search and indexing.

    Args:
        request: TTSRequest containing text to embed.
        model: OpenAI embedding model ID.
        api_key: OpenAI API key.

    Returns:
        Dict with embedding vector, metadata, and request info.
    """
    embedding = embed_script(request.text, model=model, api_key=api_key)

    return {
        "embedding": embedding,
        "model": model,
        "text": request.text,
        "voice_id": request.voice_id,
        "language_code": request.language_code,
        "embedding_dimensions": len(embedding),
    }


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Compute cosine similarity between two embedding vectors."""
    import math
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def search_similar_scripts(
    query_text: str,
    script_embeddings: List[Dict[str, Any]],
    top_k: int = 5,
    model: str = OPENAI_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Search for similar narration scripts using OpenAI embeddings.

    Args:
        query_text: The query text to search for.
        script_embeddings: List of dicts with 'embedding', 'text', and metadata.
        top_k: Number of top results to return.
        model: OpenAI embedding model ID.
        api_key: OpenAI API key.

    Returns:
        List of matching scripts sorted by similarity, with score added.
    """
    query_embedding = embed_script(query_text, model=model, api_key=api_key)

    scored = []
    for item in script_embeddings:
        sim = cosine_similarity(query_embedding, item["embedding"])
        scored.append({**item, "similarity_score": sim})

    scored.sort(key=lambda x: x["similarity_score"], reverse=True)
    return scored[:top_k]


if __name__ == "__main__":
    emb = embed_script("Hello world, this is a narration script for testing embeddings.")
    print(f"Embedding dimensions: {len(emb)}")
    print(f"First 5 values: {emb[:5]}")
