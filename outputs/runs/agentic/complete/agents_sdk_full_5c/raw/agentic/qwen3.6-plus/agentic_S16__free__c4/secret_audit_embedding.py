"""Embed secret audit notes for semantic search using OpenAI Embeddings API."""

import os
from datetime import datetime
from typing import Optional
import openai
from openai import OpenAI
from security_models import AuditNote, SecretError


# OpenAI provider configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_EMBEDDING_MODEL = os.environ.get(
    "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
)


def _get_openai_client() -> OpenAI:
    """Create an OpenAI client for embeddings."""
    if not OPENAI_API_KEY:
        raise SecretError(
            secret_id="openai_config",
            message="OPENAI_API_KEY environment variable is not set",
            error_code="MISSING_API_KEY",
            provider="openai",
        )
    return OpenAI(api_key=OPENAI_API_KEY)


def embed_audit_note(note: AuditNote, dimensions: int = None) -> dict:
    """Embed a secret audit note using OpenAI text-embedding-3-small model.

    Creates a vector embedding of the audit note text for semantic search.
    The embedding model text-embedding-3-small is used by default.

    Args:
        note: The AuditNote to embed.
        dimensions: Optional output dimensions for the embedding vector.

    Returns:
        Dict with:
            - secret_id: the audit note's secret ID
            - action: the action type
            - embedding: list of float values (the vector)
            - model: the OpenAI model used
            - provider: "openai"
    """
    text_to_embed = (
        f"Secret: {note.secret_id}, Action: {note.action}, "
        f"Operator: {note.operator}, Notes: {note.notes}"
    )

    client = _get_openai_client()
    params = {
        "model": OPENAI_EMBEDDING_MODEL,
        "input": text_to_embed,
    }
    if dimensions:
        params["dimensions"] = dimensions

    try:
        response = client.embeddings.create(**params)
        embedding = response.data[0].embedding
        return {
            "secret_id": note.secret_id,
            "action": note.action,
            "embedding": embedding,
            "model": OPENAI_EMBEDDING_MODEL,
            "provider": "openai",
        }
    except openai.APIError as exc:
        raise SecretError(
            secret_id=note.secret_id,
            message=f"OpenAI embeddings API error: {exc}",
            error_code="OPENAI_API_ERROR",
            provider="openai",
        )


def embed_audit_notes(
    notes: list[AuditNote], dimensions: int = None
) -> list[dict]:
    """Embed multiple audit notes for semantic search via OpenAI text-embedding-3-small.

    Args:
        notes: List of AuditNote objects to embed.
        dimensions: Optional output dimensions for embeddings.

    Returns:
        List of embedding result dicts.
    """
    results = []
    for note in notes:
        result = embed_audit_note(note, dimensions=dimensions)
        results.append(result)
    return results


def search_similar_audit_notes(
    query: str,
    existing_embeddings: list[dict],
    top_k: int = 5,
) -> list[dict]:
    """Search for audit notes similar to a query using OpenAI embeddings.

    Embeds the query using text-embedding-3-small, then computes cosine similarity
    against pre-computed embeddings to find the top_k most similar audit notes.

    Args:
        query: The search query text.
        existing_embeddings: List of pre-computed embedding dicts from embed_audit_note.
        top_k: Number of results to return.

    Returns:
        List of the top_k most similar embedding results, sorted by similarity.
    """
    import numpy as np

    client = _get_openai_client()
    try:
        query_response = client.embeddings.create(
            model=OPENAI_EMBEDDING_MODEL,
            input=query,
        )
        query_vector = np.array(query_response.data[0].embedding)
    except openai.APIError as exc:
        raise SecretError(
            secret_id="query",
            message=f"OpenAI embeddings API error during search: {exc}",
            error_code="OPENAI_API_ERROR",
            provider="openai",
        )

    similarities = []
    for item in existing_embeddings:
        item_vector = np.array(item["embedding"])
        norm_query = np.linalg.norm(query_vector)
        norm_item = np.linalg.norm(item_vector)
        if norm_query == 0 or norm_item == 0:
            similarity = 0.0
        else:
            similarity = float(np.dot(query_vector, item_vector) / (norm_query * norm_item))
        similarities.append((similarity, item))

    similarities.sort(key=lambda x: x[0], reverse=True)
    return [
        {"similarity": sim, **item} for sim, item in similarities[:top_k]
    ]


if __name__ == "__main__":
    test_note = AuditNote(
        secret_id="prod/api/key",
        action="ROTATE",
        timestamp=datetime.now(),
        notes="Rotated API key after quarterly security review",
        operator="admin@example.com",
    )
    result = embed_audit_note(test_note)
    print(f"Embedding created with model {result['model']} ({len(result['embedding'])} dimensions)")
