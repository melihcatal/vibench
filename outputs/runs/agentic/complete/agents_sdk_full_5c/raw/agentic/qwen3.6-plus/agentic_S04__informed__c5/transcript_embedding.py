"""
Embed transcript segments for semantic retrieval using OpenAI Embeddings API.

Generates vector embeddings for each transcript segment using the
OpenAI text-embedding-3-small model for downstream semantic search.
"""

import os
import json
from typing import List, Optional, Dict, Tuple

from openai import OpenAI

from speech_models import TranscriptionSegment, TranscriptionResult


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def get_openai_client() -> OpenAI:
    """
    Create an OpenAI client for the Embeddings API.

    Returns:
        Configured OpenAI client instance.

    Raises:
        EnvironmentError: If OPENAI_API_KEY is not set.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY environment variable is required for OpenAI embeddings"
        )

    return OpenAI(api_key=api_key)


def embed_text(
    text: str,
    model: str = OPENAI_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
) -> List[float]:
    """
    Generate an embedding vector for a single text string using OpenAI.

    Uses the OpenAI text-embedding-3-small model by default, which produces
    1536-dimensional embeddings.

    Args:
        text: The input text to embed.
        model: OpenAI embedding model name (default: text-embedding-3-small).
        dimensions: Optional output dimensionality for truncation.

    Returns:
        List of floats representing the embedding vector.

    Raises:
        openai.OpenAIError: If the API call fails.
    """
    client = get_openai_client()

    kwargs = {
        "input": text,
        "model": model,
    }

    if dimensions is not None:
        kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**kwargs)

    return response.data[0].embedding


def embed_segment(
    segment: TranscriptionSegment,
    model: str = OPENAI_EMBEDDING_MODEL,
    include_speaker: bool = True,
) -> Dict:
    """
    Embed a single transcript segment with metadata using OpenAI.

    Optionally includes the speaker label in the embedded text to improve
    semantic retrieval with speaker context.

    Args:
        segment: The TranscriptionSegment to embed.
        model: OpenAI embedding model to use.
        include_speaker: Whether to prepend speaker label to text.

    Returns:
        Dict with segment metadata and its embedding vector.
    """
    text_to_embed = segment.text

    if include_speaker and segment.speaker_label:
        text_to_embed = f"[{segment.speaker_label}] {segment.text}"

    embedding = embed_text(text_to_embed, model=model)

    return {
        "text": segment.text,
        "speaker_label": segment.speaker_label,
        "start_time_ms": segment.start_time_ms,
        "end_time_ms": segment.end_time_ms,
        "embedding": embedding,
        "model": model,
        "dimension": len(embedding),
    }


def embed_transcript_segments(
    transcript_result: TranscriptionResult,
    model: str = OPENAI_EMBEDDING_MODEL,
    batch_size: int = 100,
    include_speaker: bool = True,
) -> List[Dict]:
    """
    Embed all segments of a transcript using the OpenAI Embeddings API.

    Processes segments in batches for efficient API usage with the
    OpenAI text-embedding-3-small model.

    Args:
        transcript_result: The TranscriptionResult to embed.
        model: OpenAI embedding model name (default: text-embedding-3-small).
        batch_size: Number of segments to embed per API call.
        include_speaker: Whether to include speaker labels in embeddings.

    Returns:
        List of dicts, each containing segment metadata and embedding vector.
    """
    client = get_openai_client()
    all_results = []

    for i in range(0, len(transcript_result.segments), batch_size):
        batch = transcript_result.segments[i : i + batch_size]

        texts = []
        for segment in batch:
            text = segment.text
            if include_speaker and segment.speaker_label:
                text = f"[{segment.speaker_label}] {segment.text}"
            texts.append(text)

        response = client.embeddings.create(
            input=texts,
            model=model,
        )

        for j, seg in enumerate(batch):
            embedding_data = response.data[j]
            all_results.append(
                {
                    "text": seg.text,
                    "speaker_label": seg.speaker_label,
                    "start_time_ms": seg.start_time_ms,
                    "end_time_ms": seg.end_time_ms,
                    "embedding": embedding_data.embedding,
                    "model": model,
                    "dimension": len(embedding_data.embedding),
                }
            )

    return all_results


def build_retrieval_index(
    embedded_segments: List[Dict],
) -> Dict:
    """
    Build a lightweight retrieval index from embedded transcript segments.

    Creates a structure suitable for in-memory semantic search using
    OpenAI embedding vectors.

    Args:
        embedded_segments: List of segment dicts with embeddings.

    Returns:
        Index dict with vectors, metadata, and model info.
    """
    if not embedded_segments:
        return {"vectors": [], "metadata": [], "model": None}

    vectors = [entry["embedding"] for entry in embedded_segments]
    metadata = [
        {
            "text": entry["text"],
            "speaker_label": entry["speaker_label"],
            "start_time_ms": entry["start_time_ms"],
            "end_time_ms": entry["end_time_ms"],
        }
        for entry in embedded_segments
    ]

    return {
        "vectors": vectors,
        "metadata": metadata,
        "model": embedded_segments[0].get("model"),
        "dimension": embedded_segments[0].get("dimension", 0),
        "count": len(embedded_segments),
    }


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """
    Compute cosine similarity between two embedding vectors.

    Args:
        vec_a: First vector (from OpenAI text-embedding-3-small).
        vec_b: Second vector.

    Returns:
        Cosine similarity score between -1 and 1.
    """
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = sum(a * a for a in vec_a) ** 0.5
    norm_b = sum(b * b for b in vec_b) ** 0.5

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


def semantic_search(
    query: str,
    index: Dict,
    top_k: int = 5,
    model: str = OPENAI_EMBEDDING_MODEL,
) -> List[Tuple[float, Dict]]:
    """
    Perform semantic search over embedded transcript segments using OpenAI.

    Embeds the query with the same OpenAI model and finds the most similar
    transcript segments via cosine similarity.

    Args:
        query: The search query text.
        index: Retrieval index from build_retrieval_index.
        top_k: Number of top results to return.
        model: OpenAI embedding model for query embedding.

    Returns:
        List of (similarity_score, metadata) tuples sorted by relevance.
    """
    query_embedding = embed_text(query, model=model)

    scores = []
    for vector, meta in zip(index["vectors"], index["metadata"]):
        sim = cosine_similarity(query_embedding, vector)
        scores.append((sim, meta))

    scores.sort(key=lambda x: x[0], reverse=True)

    return scores[:top_k]
