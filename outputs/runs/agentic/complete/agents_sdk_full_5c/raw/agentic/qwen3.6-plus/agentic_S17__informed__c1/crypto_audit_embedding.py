"""
Embed crypto audit notes for semantic search using OpenAI Embeddings API.
OpenAI / Azure OpenAI embeddings (openai SDK) is the concrete provider.

This module generates embeddings for cryptographic audit notes using
OpenAI's text-embedding-3-small model for semantic search and similarity.
"""

import os
import json
from typing import List, Dict, Any, Optional

from openai import OpenAI

from security_models import format_audit_note


# OpenAI embedding model identifier
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_audit_note(
    note: str,
    model: str = OPENAI_EMBEDDING_MODEL,
) -> List[float]:
    """
    Generate an embedding for a single crypto audit note using OpenAI.

    Uses OpenAI Embeddings API with text-embedding-3-small model.

    Args:
        note: The audit note text to embed.
        model: OpenAI embedding model identifier.

    Returns:
        List of floats representing the embedding vector.

    Raises:
        ValueError: If note is empty.
        openai.APIError: If OpenAI API call fails.
    """
    if not note:
        raise ValueError("audit note cannot be empty")

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))

    response = client.embeddings.create(
        model=model,
        input=note,
    )

    embedding = response.data[0].embedding
    return embedding


def embed_multiple_audit_notes(
    notes: List[str],
    model: str = OPENAI_EMBEDDING_MODEL,
) -> List[List[float]]:
    """
    Generate embeddings for multiple audit notes using OpenAI.

    Args:
        notes: List of audit note strings.
        model: OpenAI embedding model identifier.

    Returns:
        List of embedding vectors.
    """
    if not notes:
        return []

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))

    response = client.embeddings.create(
        model=model,
        input=notes,
    )

    # Sort by index to ensure order matches input
    embeddings = sorted(
        [item.embedding for item in response.data],
        key=lambda x: response.data.index(
            next(i for i in response.data if i.embedding == x)
        ),
    )

    return [item.embedding for item in sorted(response.data, key=lambda x: x.index)]


def embed_audit_events(
    events: List[Dict[str, Any]],
    model: str = OPENAI_EMBEDDING_MODEL,
) -> List[Dict[str, Any]]:
    """
    Embed a list of audit events with metadata using OpenAI.

    Args:
        events: List of event dicts with keys like operation, key_id, success.
        model: OpenAI embedding model.

    Returns:
        List of dicts with original event data and embeddings.
    """
    notes = []
    for event in events:
        note = format_audit_note(
            operation=event.get("operation", "Unknown"),
            key_id=event.get("key_id", "unknown"),
            success=event.get("success", False),
            details=event.get("details", ""),
        )
        notes.append(note)

    embeddings = embed_multiple_audit_notes(notes, model=model)

    results = []
    for event, note, embedding in zip(events, notes, embeddings):
        results.append({
            "event": event,
            "note": note,
            "embedding": embedding,
            "model": model,
        })

    return results


def find_similar_audit_notes(
    query: str,
    embedded_notes: List[Dict[str, Any]],
    top_k: int = 5,
) -> List[Dict[str, Any]]:
    """
    Find the most similar audit notes to a query using cosine similarity.

    Args:
        query: The search query text.
        embedded_notes: List of embedded notes from embed_audit_events.
        top_k: Number of results to return.

    Returns:
        Top-k most similar notes with similarity scores.
    """
    import math

    query_embedding = embed_audit_note(query)

    def cosine_similarity(a: List[float], b: List[float]) -> float:
        dot_product = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot_product / (norm_a * norm_b)

    scored_notes = []
    for item in embedded_notes:
        similarity = cosine_similarity(query_embedding, item["embedding"])
        scored_notes.append({
            "note": item["note"],
            "event": item["event"],
            "similarity": similarity,
        })

    scored_notes.sort(key=lambda x: x["similarity"], reverse=True)
    return scored_notes[:top_k]


def main():
    """CLI entry point for crypto_audit_embedding."""
    notes_json = os.environ.get("AUDIT_NOTES", "[]")
    query = os.environ.get("SEARCH_QUERY", "")

    try:
        notes_data = json.loads(notes_json)
    except json.JSONDecodeError:
        notes_data = [
            {"operation": "Encrypt", "key_id": "key-123", "success": True, "details": "Encrypted payload"},
            {"operation": "Decrypt", "key_id": "key-456", "success": False, "details": "Invalid ciphertext"},
            {"operation": "Sign", "key_id": "key-789", "success": True, "details": "Message signed"},
        ]

    # Embed notes
    embedded = embed_audit_events(notes_data)
    print(f"Embedded {len(embedded)} audit notes using {OPENAI_EMBEDDING_MODEL}")

    if query:
        similar = find_similar_audit_notes(query, embedded, top_k=3)
        print(f"\nTop results for query '{query}':")
        for result in similar:
            print(f"  [{result['similarity']:.4f}] {result['note']}")
    else:
        for item in embedded:
            print(f"  Note: {item['note']}")
            print(f"  Embedding length: {len(item['embedding'])}")


if __name__ == "__main__":
    main()
