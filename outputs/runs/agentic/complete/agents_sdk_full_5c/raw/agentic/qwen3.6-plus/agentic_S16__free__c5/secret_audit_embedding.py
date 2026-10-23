"""
secret_audit_embedding.py - Embed secret audit notes for semantic search.

Uses OpenAI embeddings API (api.openai.com) to generate vector embeddings
for secret audit notes, enabling semantic similarity search across audit
log entries for security investigations and compliance reviews.

Provider: OpenAI Embeddings API (api.openai.com)
"""

from __future__ import annotations

import logging
import os
from typing import Dict, List, Optional, Tuple

import openai
from openai import OpenAI

from security_models import AuditNote, normalize_datetime

logger = logging.getLogger(__name__)

# Provider-specific OpenAI API configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_EMBEDDING_DIMENSIONS = 1536


def get_openai_client() -> Optional[OpenAI]:
    """Create an OpenAI client for the embeddings API."""
    if not OPENAI_API_KEY:
        logger.warning("OPENAI_API_KEY environment variable not set")
        return None
    client = OpenAI(api_key=OPENAI_API_KEY)
    return client


def generate_embedding(
    text: str,
    model: str = OPENAI_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
) -> Optional[List[float]]:
    """
    Generate an embedding vector for the given text using OpenAI's embedding model.

    Args:
        text: The text to embed.
        model: The OpenAI embedding model ID (default: text-embedding-3-small).
        dimensions: Optional dimensionality of the output embedding.

    Returns:
        List of floats representing the embedding vector, or None on failure.
    """
    client = get_openai_client()
    if not client:
        return None

    if not text.strip():
        return None

    try:
        kwargs: dict = {"model": model, "input": text}
        if dimensions:
            kwargs["dimensions"] = dimensions

        response = client.embeddings.create(**kwargs)
        if response.data:
            return response.data[0].embedding
        return None
    except Exception as e:
        logger.error("OpenAI embeddings API error: %s", e)
        return None


def embed_audit_note(audit_note: AuditNote) -> AuditNote:
    """
    Generate an embedding for an audit note's text content.

    Args:
        audit_note: The AuditNote to enrich with an embedding.

    Returns:
        The same AuditNote with the embedding field populated.
    """
    embedding_text = f"Operation: {audit_note.operation} on secret {audit_note.secret_id}. Notes: {audit_note.note_text}"
    embedding = generate_embedding(embedding_text)
    if embedding:
        audit_note.embedding = embedding
    return audit_note


def embed_audit_notes(notes: List[AuditNote]) -> List[AuditNote]:
    """
    Generate embeddings for a batch of audit notes.

    Uses the OpenAI batch API for efficiency with larger sets.

    Args:
        notes: List of AuditNote objects to embed.

    Returns:
        List of AuditNote objects with embeddings populated.
    """
    client = get_openai_client()
    if not client or not notes:
        return notes

    texts = [
        f"Operation: {note.operation} on secret {note.secret_id}. Notes: {note.note_text}"
        for note in notes
    ]

    try:
        response = client.embeddings.create(
            model=OPENAI_EMBEDDING_MODEL,
            input=texts,
            dimensions=OPENAI_EMBEDDING_DIMENSIONS,
        )

        for i, data in enumerate(response.data):
            if i < len(notes):
                notes[i].embedding = data.embedding

    except Exception as e:
        logger.error("OpenAI batch embeddings error: %s", e)
        for note in notes:
            if note.embedding is None:
                note.embedding = generate_embedding(
                    f"Operation: {note.operation} on secret {note.secret_id}. Notes: {note.note_text}"
                )

    return notes


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Compute cosine similarity between two embedding vectors."""
    if not vec_a or not vec_b:
        return 0.0
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = sum(a * a for a in vec_a) ** 0.5
    magnitude_b = sum(b * b for b in vec_b) ** 0.0 if (sum(b * b for b in vec_b)) == 0 else sum(b * b for b in vec_b) ** 0.5
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)


def search_similar_audit_notes(
    query_text: str,
    indexed_notes: List[AuditNote],
    top_k: int = 5,
) -> List[Tuple[AuditNote, float]]:
    """
    Search for audit notes semantically similar to the query text.

    Args:
        query_text: The search query text.
        indexed_notes: List of previously embedded AuditNote objects.
        top_k: Number of top results to return.

    Returns:
        List of (AuditNote, similarity_score) tuples sorted by relevance.
    """
    query_embedding = generate_embedding(query_text)
    if not query_embedding:
        return []

    scored = []
    for note in indexed_notes:
        if note.embedding:
            score = cosine_similarity(query_embedding, note.embedding)
            note.similarity_score = score
            scored.append((note, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]


def build_audit_search_index(
    notes: List[AuditNote],
) -> Dict[str, AuditNote]:
    """
    Build a searchable index of audit notes with embeddings.

    Args:
        notes: List of AuditNote objects.

    Returns:
        Dictionary mapping note_id to embedded AuditNote.
    """
    embedded = embed_audit_notes(notes)
    return {note.note_id: note for note in embedded if note.embedding}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sample_notes = [
        AuditNote(
            note_id="n1", secret_id="secret-1",
            timestamp=normalize_datetime("2024-01-15T10:00:00Z") or normalize_datetime("2024-01-15T10:00:00"),
            operation="rotation", operator="admin",
            note_text="Rotated API key due to potential compromise"
        ),
        AuditNote(
            note_id="n2", secret_id="secret-2",
            timestamp=normalize_datetime("2024-01-16T14:00:00Z") or normalize_datetime("2024-01-16T14:00:00"),
            operation="access", operator="service-account",
            note_text="Application retrieved database credentials"
        ),
    ]
    index = build_audit_search_index(sample_notes)
    results = search_similar_audit_notes("security incident credential leak", list(index.values()))
    for note, score in results:
        print(f"[{score:.3f}] {note.operation}: {note.note_text}")
