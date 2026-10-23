"""
crypto_audit_embedding.py - Embed crypto audit notes for semantic search using OpenAI embeddings.

Provider: OpenAI Embeddings API
Service endpoint: api.openai.com
Concrete model: text-embedding-3-small
"""

from __future__ import annotations

import hashlib
import os
import uuid
from typing import Any, Dict, List, Optional

from openai import OpenAI

from security_models import CryptoAuditNote, format_audit_note


class AuditEmbeddingStore:
    """In-memory store for embedded audit notes with OpenAI embeddings."""

    def __init__(self):
        self.embeddings: List[Dict[str, Any]] = []

    def add(self, note_id: str, text: str, embedding: List[float], metadata: Optional[Dict] = None):
        self.embeddings.append({
            "note_id": note_id,
            "text": text,
            "embedding": embedding,
            "metadata": metadata or {},
        })

    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        results = []
        for entry in self.embeddings:
            similarity = cosine_similarity(query_embedding, entry["embedding"])
            results.append({
                **entry,
                "similarity": similarity,
            })
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Compute cosine similarity between two vectors."""
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = sum(a * a for a in vec_a) ** 0.5
    norm_b = sum(b * b for b in vec_b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def create_openai_client(
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
    base_url: Optional[str] = None,
) -> OpenAI:
    """
    Create an OpenAI client for embedding generation.

    Uses api.openai.com endpoint with the text-embedding-3-small model
    from OpenAI's embedding family for semantic search of audit notes.

    Args:
        api_key: OpenAI API key. Defaults to OPENAI_API_KEY env var.
        organization: Optional OpenAI organization ID.
        base_url: Optional custom base URL.

    Returns:
        Configured OpenAI client.
    """
    kwargs: Dict[str, Any] = {
        "api_key": api_key or os.environ.get("OPENAI_API_KEY", ""),
    }
    if organization:
        kwargs["organization"] = organization
    if base_url:
        kwargs["base_url"] = base_url

    return OpenAI(**kwargs)


def generate_embedding(
    text: str,
    model: str = "text-embedding-3-small",
    dimensions: Optional[int] = None,
    client: Optional[OpenAI] = None,
) -> List[float]:
    """
    Generate an embedding vector for text using OpenAI text-embedding-3-small model.

    Args:
        text: Text to embed (audit note or query).
        model: OpenAI embedding model ID (default: text-embedding-3-small).
        dimensions: Optional output dimensionality.
        client: Pre-configured OpenAI client.

    Returns:
        Embedding vector as a list of floats.
    """
    if client is None:
        client = create_openai_client()

    params: Dict[str, Any] = {
        "model": model,
        "input": text,
    }

    if dimensions is not None:
        params["dimensions"] = dimensions

    response = client.embeddings.create(**params)

    return response.data[0].embedding


def embed_audit_notes(
    notes: List[CryptoAuditNote],
    model: str = "text-embedding-3-small",
    client: Optional[OpenAI] = None,
    store: Optional[AuditEmbeddingStore] = None,
) -> AuditEmbeddingStore:
    """
    Embed multiple crypto audit notes for semantic search.

    Each note is formatted and then embedded using OpenAI's
    text-embedding-3-small model via api.openai.com.

    Args:
        notes: List of CryptoAuditNote objects to embed.
        model: OpenAI embedding model (default: text-embedding-3-small).
        client: Optional pre-configured OpenAI client.
        store: Optional existing store to add to.

    Returns:
        AuditEmbeddingStore containing embedded notes.
    """
    if store is None:
        store = AuditEmbeddingStore()

    if client is None:
        client = create_openai_client()

    for note in notes:
        formatted_text = format_audit_note(note)
        embedding = generate_embedding(formatted_text, model=model, client=client)

        store.add(
            note_id=note.note_id,
            text=formatted_text,
            embedding=embedding,
            metadata={
                "key_id": note.key_id,
                "severity": note.severity,
                "created_at": note.created_at,
                "original_text": note.note_text,
            },
        )

    return store


def search_audit_notes(
    query: str,
    store: AuditEmbeddingStore,
    model: str = "text-embedding-3-small",
    top_k: int = 5,
    client: Optional[OpenAI] = None,
) -> List[Dict[str, Any]]:
    """
    Search embedded audit notes using a natural language query.

    Embeds the query using OpenAI text-embedding-3-small and performs
    cosine similarity search against the stored embeddings.

    Args:
        query: Natural language search query.
        store: AuditEmbeddingStore with pre-embedded notes.
        model: OpenAI embedding model to use.
        top_k: Number of results to return.
        client: Optional pre-configured OpenAI client.

    Returns:
        List of matching notes with similarity scores.
    """
    if client is None:
        client = create_openai_client()

    query_embedding = generate_embedding(query, model=model, client=client)
    return store.search(query_embedding, top_k=top_k)


if __name__ == "__main__":
    sample_notes = [
        CryptoAuditNote(
            note_id=str(uuid.uuid4()),
            key_id="arn:aws:kms:us-east-1:123456789012:key/example-key-1",
            note_text="Key rotation overdue by 30 days. Recommend immediate rotation.",
            severity="HIGH",
            created_at="2024-01-15T10:00:00Z",
        ),
        CryptoAuditNote(
            note_id=str(uuid.uuid4()),
            key_id="arn:aws:kms:us-east-1:123456789012:key/example-key-2",
            note_text="Encryption context mismatch detected in decrypt operation.",
            severity="MEDIUM",
            created_at="2024-01-16T14:30:00Z",
        ),
    ]

    store = embed_audit_notes(sample_notes)
    print(f"Embedded {len(store.embeddings)} audit notes")

    results = search_audit_notes("key rotation issues", store)
    for r in results:
        print(f"  [{r['metadata']['severity']}] {r['text']} (similarity: {r['similarity']:.3f})")
