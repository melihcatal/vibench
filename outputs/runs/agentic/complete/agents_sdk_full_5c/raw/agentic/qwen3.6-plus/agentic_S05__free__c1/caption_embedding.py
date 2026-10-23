"""Embed caption chunks for semantic meeting search using OpenAI Embeddings API.

Uses the OpenAI text-embedding-ada-002 model via the OpenAI Embeddings API
to create vector embeddings of caption chunks for semantic search over meetings.
"""

import os
from typing import Dict, List, Optional, Tuple

import openai
from openai import OpenAI

from speech_models import clean_transcript_text, TranscriptSegment

# OpenAI Embeddings API base URL
OPENAI_EMBEDDING_API_BASE = "https://api.openai.com/v1"

# OpenAI embedding model identifier
OPENAI_EMBEDDING_MODEL = "text-embedding-ada-002"

# Default embedding dimension for text-embedding-ada-002
EMBEDDING_DIMENSION = 1536


def get_openai_client() -> OpenAI:
    """Create an OpenAI API client for embeddings.

    Returns:
        Configured OpenAI client using the OPENAI_API_KEY environment variable.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable must be set for OpenAI Embeddings API access."
        )
    return OpenAI(api_key=api_key, base_url=OPENAI_EMBEDDING_API_BASE)


def embed_caption_chunk(
    text: str,
    model: str = OPENAI_EMBEDDING_MODEL,
) -> List[float]:
    """Generate an embedding for a single caption chunk using OpenAI text-embedding-ada-002.

    Args:
        text: The caption text to embed.
        model: OpenAI embedding model identifier (default: text-embedding-ada-002).

    Returns:
        List of floats representing the embedding vector.
    """
    client = get_openai_client()
    cleaned = clean_transcript_text(text)

    if not cleaned:
        return [0.0] * EMBEDDING_DIMENSION

    response = client.embeddings.create(
        model=model,
        input=cleaned,
    )

    return response.data[0].embedding


def embed_caption_chunks_batch(
    texts: List[str],
    model: str = OPENAI_EMBEDDING_MODEL,
) -> List[List[float]]:
    """Generate embeddings for multiple caption chunks via OpenAI embeddings API.

    Uses the OpenAI text-embedding-ada-002 model to embed multiple texts
    in a single API call for efficiency.

    Args:
        texts: List of caption text strings to embed.
        model: OpenAI embedding model identifier (default: text-embedding-ada-002).

    Returns:
        List of embedding vectors, one per input text.
    """
    client = get_openai_client()
    cleaned_texts = [clean_transcript_text(t) for t in texts if t.strip()]

    if not cleaned_texts:
        return []

    response = client.embeddings.create(
        model=model,
        input=cleaned_texts,
    )

    sorted_data = sorted(response.data, key=lambda x: x.index)
    return [item.embedding for item in sorted_data]


def embed_streaming_captions(
    transcript_events,
    model: str = OPENAI_EMBEDDING_MODEL,
):
    """Process a stream of recognition events and yield embeddings for final transcripts.

    Generates OpenAI text-embedding-ada-002 embeddings for each final caption
    segment from the streaming speech-to-text pipeline.

    Args:
        transcript_events: Iterator of (transcript, is_final, confidence) tuples.
        model: OpenAI embedding model identifier.

    Yields:
        Tuples of (transcript, is_final, confidence, embedding_vector) for final results.
    """
    for transcript, is_final, confidence in transcript_events:
        if not is_final:
            continue

        embedding = embed_caption_chunk(transcript, model=model)
        yield transcript, is_final, confidence, embedding


def compute_similarity(embedding_a: List[float], embedding_b: List[float]) -> float:
    """Compute cosine similarity between two embedding vectors.

    Args:
        embedding_a: First embedding vector.
        embedding_b: Second embedding vector.

    Returns:
        Cosine similarity score between 0.0 and 1.0.
    """
    if len(embedding_a) != len(embedding_b):
        raise ValueError("Embedding vectors must have the same dimension")

    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    norm_a = sum(a * a for a in embedding_a) ** 0.5
    norm_b = sum(b * b for b in embedding_b) ** 0.5

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


def build_meeting_index(
    transcript_events,
    model: str = OPENAI_EMBEDDING_MODEL,
) -> List[Dict]:
    """Build a semantic search index from a stream of meeting captions.

    Uses the OpenAI text-embedding-ada-002 model to create embeddings for
    all final transcript segments, building an index suitable for semantic search.

    Args:
        transcript_events: Iterator of (transcript, is_final, confidence) tuples.
        model: OpenAI embedding model identifier.

    Returns:
        List of dicts with keys: index, transcript, confidence, embedding.
    """
    index = []
    for idx, (transcript, is_final, confidence) in enumerate(transcript_events):
        if not is_final:
            continue

        cleaned = clean_transcript_text(transcript)
        if not cleaned:
            continue

        embedding = embed_caption_chunk(cleaned, model=model)
        index.append({
            "index": idx,
            "transcript": cleaned,
            "confidence": confidence,
            "embedding": embedding,
        })

    return index


def search_meeting_index(
    query: str,
    index: List[Dict],
    top_k: int = 5,
    model: str = OPENAI_EMBEDDING_MODEL,
) -> List[Tuple[Dict, float]]:
    """Search the meeting index using semantic similarity via OpenAI embeddings.

    Embeds the query using text-embedding-ada-002 and finds the most
    similar meeting transcript chunks by cosine similarity.

    Args:
        query: Search query text.
        index: Meeting index built by build_meeting_index.
        top_k: Number of top results to return.
        model: OpenAI embedding model identifier.

    Returns:
        List of (entry, similarity_score) tuples sorted by similarity descending.
    """
    query_embedding = embed_caption_chunk(query, model=model)

    scored = []
    for entry in index:
        similarity = compute_similarity(query_embedding, entry["embedding"])
        scored.append((entry, similarity))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]
