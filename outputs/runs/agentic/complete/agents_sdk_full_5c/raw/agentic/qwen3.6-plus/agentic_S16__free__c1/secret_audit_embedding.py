"""
secret_audit_embedding.py - Embed secret audit notes for semantic search using OpenAI.

Uses the OpenAI API (api.openai.com) with the text-embedding-3-small model
to generate vector embeddings of secret audit notes, enabling semantic search
and similarity-based retrieval of audit records.
"""

from __future__ import annotations

import logging
import os
from typing import Optional, Dict, Any, List

from openai import OpenAI

from security_models import AuditNotePayload

logger = logging.getLogger(__name__)

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_API_BASE = "https://api.openai.com/v1"


def get_openai_client() -> OpenAI:
    """Create an OpenAI client using the OPENAI_API_KEY environment variable."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key, base_url=OPENAI_API_BASE)


def embed_audit_note(
    audit_note: str,
    secret_name: str = "",
    model: str = OPENAI_EMBEDDING_MODEL,
) -> Dict[str, Any]:
    """
    Generate an embedding for a secret audit note using OpenAI text-embedding-3-small.

    Args:
        audit_note: The audit note text to embed.
        secret_name: Optional secret name for context.
        model: OpenAI embedding model identifier (default: text-embedding-3-small).

    Returns:
        Dict with the embedding vector, model info, and metadata.
    """
    client = get_openai_client()
    logger.info("Embedding audit note for %s using OpenAI %s", secret_name or "unknown", model)

    try:
        response = client.embeddings.create(
            model=model,
            input=audit_note,
            encoding_format="float",
        )

        embedding_data = response.data[0]
        result = {
            "secret_name": secret_name,
            "embedding": embedding_data.embedding,
            "model": model,
            "usage_tokens": response.usage.total_tokens,
            "note_length": len(audit_note),
            "payload": AuditNotePayload(
                secret_name=secret_name,
                audit_note=audit_note,
            ).to_json(),
        }

        logger.info(
            "Generated embedding for %s: dim=%d, tokens=%d",
            secret_name or "unknown",
            len(embedding_data.embedding),
            response.usage.total_tokens,
        )
        return result

    except Exception as e:
        logger.error("OpenAI embedding failed for %s: %s", secret_name or "unknown", e)
        raise


def embed_batch_audit_notes(
    notes: List[AuditNotePayload],
    model: str = OPENAI_EMBEDDING_MODEL,
) -> List[Dict[str, Any]]:
    """
    Generate embeddings for a batch of audit notes using OpenAI.

    Args:
        notes: List of AuditNotePayload objects to embed.
        model: OpenAI embedding model identifier.

    Returns:
        List of embedding result dicts.
    """
    client = get_openai_client()
    texts = [note.audit_note for note in notes]

    logger.info("Embedding batch of %d audit notes using OpenAI %s", len(texts), model)

    try:
        response = client.embeddings.create(
            model=model,
            input=texts,
            encoding_format="float",
        )

        results = []
        for i, embedding_data in enumerate(response.data):
            results.append({
                "secret_name": notes[i].secret_name,
                "embedding": embedding_data.embedding,
                "model": model,
                "usage_tokens": response.usage.total_tokens,
                "note_length": len(texts[i]),
            })

        logger.info("Batch embedding complete: %d notes, total tokens=%d", len(results), response.usage.total_tokens)
        return results

    except Exception as e:
        logger.error("OpenAI batch embedding failed: %s", e)
        raise


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """
    Compute cosine similarity between two embedding vectors.

    Args:
        vec_a: First embedding vector.
        vec_b: Second embedding vector.

    Returns:
        Cosine similarity score between 0.0 and 1.0.
    """
    import math
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    note = AuditNotePayload(
        secret_name="production/db/postgres-main",
        audit_note="Rotated credentials due to quarterly compliance requirement. Old key deactivated.",
    )
    result = embed_audit_note(note.audit_note, note.secret_name)
    print(f"Embedding dimension: {len(result['embedding'])}")
    print(f"Tokens used: {result['usage_tokens']}")
