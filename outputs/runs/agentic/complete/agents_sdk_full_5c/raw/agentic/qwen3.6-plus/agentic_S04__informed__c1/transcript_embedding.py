"""Embed transcript segments for semantic retrieval using OpenAI Embeddings API."""

import os
from typing import List, Optional

import openai

from speech_models import TranscriptionResponse, TranscriptSegment


OPENAI_API_HOST = "api.openai.com"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


def create_openai_client(api_key: Optional[str] = None) -> openai.OpenAI:
    """Create an OpenAI client for the Embeddings API.

    Args:
        api_key: OpenAI API key; falls back to OPENAI_API_KEY env var.

    Returns:
        Configured openai.OpenAI client instance.
    """
    if api_key is None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable must be set")
    return openai.OpenAI(api_key=api_key)


def embed_segments(
    response: TranscriptionResponse,
    model: str = DEFAULT_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
) -> List[dict]:
    """Embed all transcript segments using OpenAI text-embedding-3-small model.

    Args:
        response: TranscriptionResponse to embed.
        model: OpenAI embedding model identifier (e.g., 'text-embedding-3-small').
        api_key: Optional OpenAI API key.

    Returns:
        List of dicts with segment text, metadata, and embedding vector.
    """
    client = create_openai_client(api_key)

    texts = [seg.text for seg in response.segments if seg.text]
    if not texts:
        return []

    batch_embeddings = []
    for i, text in enumerate(texts):
        seg = response.segments[i]
        emb_response = client.embeddings.create(
            model=model,
            input=text,
            encoding_format="float",
        )
        embedding = emb_response.data[0].embedding
        batch_embeddings.append({
            "text": text,
            "embedding": embedding,
            "segment_index": i,
            "start_ms": seg.start_ms,
            "end_ms": seg.end_ms,
            "speaker": seg.speaker,
            "model": model,
        })

    return batch_embeddings


def embed_full_transcript(
    response: TranscriptionResponse,
    model: str = DEFAULT_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    chunk_size: int = 500,
) -> List[dict]:
    """Embed the full transcript in chunks for semantic retrieval.

    Args:
        response: TranscriptionResponse to embed.
        model: OpenAI embedding model identifier.
        api_key: Optional OpenAI API key.
        chunk_size: Character count per chunk for embedding.

    Returns:
        List of dicts with chunk text and embedding vector.
    """
    client = create_openai_client(api_key)
    text = response.text

    chunks = []
    for start in range(0, len(text), chunk_size):
        end = start + chunk_size
        chunk_text = text[start:end]
        if chunk_text.strip():
            chunks.append(chunk_text)

    if not chunks:
        return []

    embeddings = []
    for i, chunk in enumerate(chunks):
        emb_response = client.embeddings.create(
            model=model,
            input=chunk,
            encoding_format="float",
        )
        embedding = emb_response.data[0].embedding
        embeddings.append({
            "text": chunk,
            "embedding": embedding,
            "chunk_index": i,
            "model": model,
        })

    return embeddings


def search_segments_by_similarity(
    query: str,
    embedded_segments: List[dict],
    top_k: int = 5,
    model: str = DEFAULT_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
) -> List[dict]:
    """Search embedded segments by semantic similarity to a query.

    Uses OpenAI embeddings for the query and cosine similarity for ranking.

    Args:
        query: Search query string.
        embedded_segments: List of dicts with embeddings from embed_segments().
        top_k: Number of top results to return.
        model: OpenAI embedding model identifier.
        api_key: Optional OpenAI API key.

    Returns:
        Top-k most similar segments with similarity scores.
    """
    client = create_openai_client(api_key)

    query_response = client.embeddings.create(
        model=model,
        input=query,
        encoding_format="float",
    )
    query_embedding = query_response.data[0].embedding

    scored = []
    for seg_data in embedded_segments:
        similarity = _cosine_similarity(query_embedding, seg_data["embedding"])
        scored.append({**seg_data, "similarity": similarity})

    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return scored[:top_k]


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    """Compute cosine similarity between two embedding vectors."""
    import math
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


if __name__ == "__main__":
    from speech_models import TranscriptionResponse, TranscriptSegment
    demo = TranscriptionResponse(
        job_id="embed-demo",
        text="Sample transcript segments for embedding.",
        segments=[
            TranscriptSegment(text="We discussed the project timeline", start_ms=0, end_ms=2500),
            TranscriptSegment(text="Budget constraints were reviewed", start_ms=2500, end_ms=5000),
        ],
    )
    print("Embedding requires OPENAI_API_KEY to be set.")
