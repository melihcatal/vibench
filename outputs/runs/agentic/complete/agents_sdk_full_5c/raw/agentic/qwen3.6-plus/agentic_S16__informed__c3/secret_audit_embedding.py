"""
secret_audit_embedding.py - Embed secret audit notes for semantic search using OpenAI Embeddings.

Provider: OpenAI Embeddings API
SDK: openai
Auth env var: OPENAI_API_KEY
Model: text-embedding-3-small
"""

import os
import logging
from typing import List, Optional, Dict, Any

from openai import OpenAI

from security_models import AuditEmbeddingResult

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
EMBEDDING_MODEL = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def _get_openai_client() -> OpenAI:
    """Create an OpenAI client using the configured API key."""
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return OpenAI(api_key=OPENAI_API_KEY)


def embed_audit_text(text: str, model: Optional[str] = None) -> AuditEmbeddingResult:
    """
    Generate an embedding vector for audit note text using OpenAI's embedding API.

    Args:
        text: The audit note text to embed.
        model: The embedding model to use. Defaults to text-embedding-3-small.

    Returns:
        AuditEmbeddingResult with the embedding vector and metadata.

    Raises:
        ValueError: If the text is empty or API key is missing.
        APIError: On OpenAI API errors.
    """
    if not text or not text.strip():
        raise ValueError("Audit text cannot be empty")

    model = model or EMBEDDING_MODEL
    client = _get_openai_client()

    response = client.embeddings.create(
        input=text,
        model=model,
    )

    embedding_data = response.data[0]
    embedding_vector = embedding_data.embedding
    token_usage = response.usage.total_tokens if response.usage else 0

    result = AuditEmbeddingResult(
        secret_name="",
        note_text=text,
        embedding=embedding_vector,
        model=model,
        token_count=token_usage,
    )
    logger.info(
        "Embedded audit text with OpenAI model %s (%d tokens)",
        model,
        token_usage,
    )
    return result


def embed_secret_audit_notes(
    secret_name: str,
    audit_notes: str,
    model: Optional[str] = None,
) -> AuditEmbeddingResult:
    """
    Embed audit notes associated with a specific secret.

    Args:
        secret_name: The name of the secret these notes relate to.
        audit_notes: The audit note text to embed.
        model: Embedding model to use.

    Returns:
        AuditEmbeddingResult with the secret name set.
    """
    result = embed_audit_text(audit_notes, model)
    result.secret_name = secret_name
    return result


def batch_embed_audit_notes(
    notes: List[Dict[str, str]],
    model: Optional[str] = None,
) -> List[AuditEmbeddingResult]:
    """
    Batch-embed multiple audit notes using OpenAI's embedding API.

    Args:
        notes: List of dicts with keys 'secret_name' and 'audit_notes'.
        model: Embedding model to use.

    Returns:
        List of AuditEmbeddingResult objects.
    """
    results = []
    for note in notes:
        secret_name = note.get("secret_name", "")
        text = note.get("audit_notes", "")
        if text.strip():
            result = embed_secret_audit_notes(secret_name, text, model)
            results.append(result)
    return results


def compute_similarity(embedding_a: List[float], embedding_b: List[float]) -> float:
    """
    Compute cosine similarity between two embedding vectors.

    Returns a value between -1.0 and 1.0.
    """
    if len(embedding_a) != len(embedding_b):
        raise ValueError("Embedding vectors must have the same dimension")

    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    magnitude_a = sum(a * a for a in embedding_a) ** 0.5
    magnitude_b = sum(b * b for b in embedding_b) ** 0.5

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def find_similar_audit_notes(
    query_text: str,
    stored_embeddings: List[AuditEmbeddingResult],
    top_k: int = 5,
    model: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Find the most similar audit notes to a query using cosine similarity.

    Args:
        query_text: The search query text.
        stored_embeddings: List of previously computed AuditEmbeddingResult objects.
        top_k: Number of top results to return.
        model: Embedding model to use for the query.

    Returns:
        List of dicts with 'secret_name', 'similarity', and 'note_text', sorted by similarity.
    """
    query_result = embed_audit_text(query_text, model)
    query_vector = query_result.embedding

    scored = []
    for stored in stored_embeddings:
        sim = compute_similarity(query_vector, stored.embedding)
        scored.append(
            {
                "secret_name": stored.secret_name,
                "similarity": round(sim, 4),
                "note_text": stored.note_text,
            }
        )

    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return scored[:top_k]
