"""
[LATER-STEP] script_embedding.py
Embed narration scripts for voice-asset search using OpenAI Embeddings API.
"""
from typing import Optional, List, Dict, Any
import os
import openai
from openai import OpenAI
from speech_models import TTSRequest


class EmbeddingError(Exception):
    """Raised when embedding generation fails."""
    pass


def get_openai_client(api_key: Optional[str] = None) -> OpenAI:
    """Create and return an OpenAI client instance."""
    key = api_key or os.environ.get("OPENAI_API_KEY", "")
    if not key:
        raise EnvironmentError(
            "OPENAI_API_KEY environment variable is not set and no api_key provided."
        )
    return OpenAI(api_key=key)


def embed_script(
    text: str,
    model: str = "text-embedding-3-small",
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
    client: Optional[OpenAI] = None,
) -> List[float]:
    """
    Generate an embedding vector for a narration script using OpenAI Embeddings.

    Args:
        text: The text to embed.
        model: OpenAI embedding model ID (e.g., "text-embedding-3-small", "text-embedding-3-large").
        dimensions: Optional number of dimensions for the embedding output.
        api_key: Optional OpenAI API key.
        client: Optional pre-built OpenAI client.

    Returns:
        List of floats representing the embedding vector.
    """
    if client is None:
        client = get_openai_client(api_key)

    kwargs: Dict[str, Any] = {"model": model, "input": text}
    if dimensions is not None:
        kwargs["dimensions"] = dimensions

    try:
        response = client.embeddings.create(**kwargs)
        return response.data[0].embedding
    except openai.OpenAIError as e:
        raise EmbeddingError(f"OpenAI embedding generation failed: {e}") from e


def embed_scripts_batch(
    texts: List[str],
    model: str = "text-embedding-3-small",
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
    client: Optional[OpenAI] = None,
) -> List[List[float]]:
    """
    Generate embedding vectors for multiple narration scripts using OpenAI Embeddings.

    Args:
        texts: List of texts to embed.
        model: OpenAI embedding model ID.
        dimensions: Optional number of dimensions for the embedding output.
        api_key: Optional OpenAI API key.
        client: Optional pre-built OpenAI client.

    Returns:
        List of embedding vectors (each a list of floats).
    """
    if client is None:
        client = get_openai_client(api_key)

    kwargs: Dict[str, Any] = {"model": model, "input": texts}
    if dimensions is not None:
        kwargs["dimensions"] = dimensions

    try:
        response = client.embeddings.create(**kwargs)
        return [item.embedding for item in response.data]
    except openai.OpenAIError as e:
        raise EmbeddingError(f"OpenAI batch embedding generation failed: {e}") from e


def embed_tts_request(
    request: TTSRequest,
    model: str = "text-embedding-3-small",
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
    client: Optional[OpenAI] = None,
) -> Dict[str, Any]:
    """
    Generate an embedding for the text in a TTSRequest.

    Args:
        request: The TTSRequest to embed.
        model: OpenAI embedding model ID.
        dimensions: Optional number of dimensions.
        api_key: Optional OpenAI API key.
        client: Optional pre-built OpenAI client.

    Returns:
        Dictionary with embedding vector and metadata.
    """
    embedding = embed_script(
        text=request.text,
        model=model,
        dimensions=dimensions,
        api_key=api_key,
        client=client,
    )

    return {
        "embedding": embedding,
        "text": request.text,
        "model": model,
        "dimensions": len(embedding),
        "voice_id": request.voice_id,
        "language_code": request.language_code,
        "provider": "openai",
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
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = sum(a * a for a in vec_a) ** 0.5
    magnitude_b = sum(b * b for b in vec_b) ** 0.5
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)


def search_similar_scripts(
    query_text: str,
    script_embeddings: List[Dict[str, Any]],
    top_k: int = 5,
    model: str = "text-embedding-3-small",
    api_key: Optional[str] = None,
    client: Optional[OpenAI] = None,
) -> List[Dict[str, Any]]:
    """
    Search for similar narration scripts using embedding-based similarity.

    Args:
        query_text: The query text to search for.
        script_embeddings: List of pre-computed script embeddings with metadata.
        top_k: Number of top results to return.
        model: OpenAI embedding model ID.
        api_key: Optional OpenAI API key.
        client: Optional pre-built OpenAI client.

    Returns:
        List of matching scripts sorted by similarity (descending).
    """
    query_embedding = embed_script(
        text=query_text,
        model=model,
        api_key=api_key,
        client=client,
    )

    scored_results = []
    for script_entry in script_embeddings:
        similarity = cosine_similarity(
            query_embedding, script_entry.get("embedding", [])
        )
        scored_results.append({
            **script_entry,
            "similarity": similarity,
        })

    scored_results.sort(key=lambda x: x["similarity"], reverse=True)
    return scored_results[:top_k]


if __name__ == "__main__":
    embedding = embed_script("Welcome to our product demonstration.")
    print(f"Generated embedding with {len(embedding)} dimensions.")
    print(f"First 5 values: {embedding[:5]}")
