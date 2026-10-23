"""
Embed caption chunks for semantic meeting search using OpenAI Embeddings API.

Generates vector embeddings for meeting transcript chunks using OpenAI's
text-embedding-3-small model, enabling semantic search over meeting content.

Requires:
    pip install openai numpy
"""

import os
import json
import time
from typing import List, Optional, Dict, Any, Tuple

import numpy as np
from openai import OpenAI

from speech_models import TranscriptChunk, TranscriptStatus

EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSION = 1536


def get_openai_client(api_key: Optional[str] = None) -> OpenAI:
    """Create an OpenAI client for embeddings.

    Args:
        api_key: OpenAI API key. Falls back to OPENAI_API_KEY env var.

    Returns:
        Configured OpenAI client instance.

    Raises:
        ValueError: If no API key is provided.
    """
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=key)


def embed_text(
    text: str,
    model: str = EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
) -> List[float]:
    """Generate an embedding vector for a single text string.

    Uses OpenAI's text-embedding-3-small model to create a dense vector
    representation of the input text.

    Args:
        text: Text to embed.
        model: OpenAI embedding model identifier (e.g., 'text-embedding-3-small').
        dimensions: Optional output dimensionality for the embedding.
        api_key: OpenAI API key.

    Returns:
        List of floats representing the embedding vector.
    """
    if not text.strip():
        return [0.0] * (dimensions or EMBEDDING_DIMENSION)

    client = get_openai_client(api_key=api_key)

    kwargs = {"model": model, "input": text}
    if dimensions:
        kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**kwargs)
    return response.data[0].embedding


def embed_caption_chunk(
    chunk: TranscriptChunk,
    model: str = EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Embed a single caption chunk with metadata.

    Args:
        chunk: TranscriptChunk to embed.
        model: OpenAI embedding model identifier.
        dimensions: Optional output dimensionality.
        api_key: OpenAI API key.

    Returns:
        Dictionary with embedding vector and chunk metadata.
    """
    embedding = embed_text(
        text=chunk.text,
        model=model,
        dimensions=dimensions,
        api_key=api_key,
    )

    return {
        "embedding": embedding,
        "text": chunk.text,
        "chunk_id": id(chunk),
        "is_final": chunk.is_final,
        "status": chunk.status.value,
        "speaker": chunk.speaker,
        "timestamp": chunk.timestamp,
        "start_time": chunk.start_time,
        "end_time": chunk.end_time,
        "confidence": chunk.confidence,
        "vector_dimension": len(embedding),
    }


def embed_caption_chunks(
    chunks: List[TranscriptChunk],
    model: str = EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
    batch_size: int = 100,
    api_key: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Embed multiple caption chunks for semantic search.

    Generates embeddings for a list of transcript chunks using OpenAI's
    embedding API, with optional batching for efficiency.

    Args:
        chunks: List of TranscriptChunk objects to embed.
        model: OpenAI embedding model identifier (e.g., 'text-embedding-3-small').
        dimensions: Optional output dimensionality.
        batch_size: Number of texts to embed in a single API call.
        api_key: OpenAI API key.

    Returns:
        List of dictionaries with embeddings and metadata.
    """
    client = get_openai_client(api_key=api_key)

    texts = [chunk.text for chunk in chunks if chunk.text.strip()]
    if not texts:
        return []

    all_embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]

        kwargs = {"model": model, "input": batch}
        if dimensions:
            kwargs["dimensions"] = dimensions

        response = client.embeddings.create(**kwargs)

        for j, data in enumerate(response.data):
            chunk_idx = i + j
            if chunk_idx < len(chunks):
                chunk = chunks[chunk_idx]
                all_embeddings.append({
                    "embedding": data.embedding,
                    "text": chunk.text,
                    "chunk_id": id(chunk),
                    "is_final": chunk.is_final,
                    "status": chunk.status.value,
                    "speaker": chunk.speaker,
                    "timestamp": chunk.timestamp,
                    "start_time": chunk.start_time,
                    "end_time": chunk.end_time,
                    "confidence": chunk.confidence,
                    "vector_dimension": len(data.embedding),
                })

    return all_embeddings


def embed_live_caption_stream(
    chunk_stream,
    model: str = EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
):
    """Embed a stream of caption chunks as they arrive.

    Args:
        chunk_stream: Iterator of TranscriptChunk objects.
        model: OpenAI embedding model identifier.
        dimensions: Optional output dimensionality.
        api_key: OpenAI API key.

    Yields:
        Dictionaries with embeddings and metadata for each chunk.
    """
    for chunk in chunk_stream:
        if not chunk.text.strip():
            continue

        result = embed_caption_chunk(
            chunk=chunk,
            model=model,
            dimensions=dimensions,
            api_key=api_key,
        )
        yield result


async def embed_live_caption_stream_async(
    chunk_stream,
    model: str = EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
):
    """Async generator to embed caption chunks from an async stream.

    Args:
        chunk_stream: Async iterator of TranscriptChunk objects.
        model: OpenAI embedding model identifier.
        dimensions: Optional output dimensionality.
        api_key: OpenAI API key.

    Yields:
        Dictionaries with embeddings and metadata.
    """
    import asyncio

    for chunk in chunk_stream:
        if not chunk.text.strip():
            continue

        embedding = embed_text(
            text=chunk.text,
            model=model,
            dimensions=dimensions,
            api_key=api_key,
        )

        yield {
            "embedding": embedding,
            "text": chunk.text,
            "chunk_id": id(chunk),
            "is_final": chunk.is_final,
            "status": chunk.status.value,
            "speaker": chunk.speaker,
            "timestamp": chunk.timestamp,
        }
        await asyncio.sleep(0)


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Compute cosine similarity between two embedding vectors.

    Args:
        vec1: First embedding vector.
        vec2: Second embedding vector.

    Returns:
        Cosine similarity score between 0 and 1.
    """
    a = np.array(vec1)
    b = np.array(vec2)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def search_embeddings(
    query: str,
    embeddings: List[Dict[str, Any]],
    top_k: int = 5,
    api_key: Optional[str] = None,
) -> List[Tuple[float, Dict[str, Any]]]:
    """Search embedded captions by semantic similarity.

    Embeds the query text and finds the most similar caption embeddings.

    Args:
        query: Search query text.
        embeddings: List of embedded caption dictionaries.
        top_k: Number of top results to return.
        api_key: OpenAI API key.

    Returns:
        List of (similarity_score, embedding_dict) tuples sorted by score.
    """
    query_embedding = embed_text(query, api_key=api_key)

    scores = []
    for emb in embeddings:
        similarity = cosine_similarity(query_embedding, emb["embedding"])
        scores.append((similarity, emb))

    scores.sort(key=lambda x: x[0], reverse=True)
    return scores[:top_k]


def save_embeddings(
    embeddings: List[Dict[str, Any]],
    file_path: str,
) -> None:
    """Save embeddings to a JSON file.

    Args:
        embeddings: List of embedding dictionaries.
        file_path: Path to save the JSON file.
    """
    with open(file_path, "w") as f:
        json.dump(embeddings, f, indent=2)


def load_embeddings(file_path: str) -> List[Dict[str, Any]]:
    """Load embeddings from a JSON file.

    Args:
        file_path: Path to the JSON file.

    Returns:
        List of embedding dictionaries.
    """
    with open(file_path, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    test_chunks = [
        TranscriptChunk(text="Welcome to the meeting.", status=TranscriptStatus.FINAL, is_final=True, speaker=1),
        TranscriptChunk(text="Let's review the project status.", status=TranscriptStatus.FINAL, is_final=True, speaker=1),
        TranscriptChunk(text="The deadline is next Friday.", status=TranscriptStatus.FINAL, is_final=True, speaker=2),
    ]

    print("Embeddings would be generated here with a valid OPENAI_API_KEY")
