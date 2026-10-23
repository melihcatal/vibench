"""
Embed secret audit notes for semantic search using OpenAI embeddings.

This module uses the OpenAI embeddings API (text-embedding-3-small model)
at api.openai.com to create vector embeddings of secret audit notes
for downstream semantic search and similarity matching.
"""

import json
import logging
from typing import Any, Dict, List, Optional

import openai
from openai import OpenAI

logger = logging.getLogger(__name__)

OPENAI_API_BASE = "https://api.openai.com/v1"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def _get_openai_client() -> OpenAI:
    """Create an OpenAI client using the official SDK."""
    return OpenAI(
        api_key=__import__("os").environ.get("OPENAI_API_KEY", ""),
        base_url=OPENAI_API_BASE,
    )


def embed_audit_notes(notes: str) -> Optional[List[float]]:
    """
    Generate an embedding vector for secret audit notes using OpenAI.

    Uses the text-embedding-3-small model via api.openai.com.

    Args:
        notes: The audit notes text to embed.

    Returns:
        List of floats representing the embedding vector, or None on failure.
    """
    try:
        client = _get_openai_client()

        response = client.embeddings.create(
            model=OPENAI_EMBEDDING_MODEL,
            input=notes,
            encoding_format="float",
        )

        if response.data and len(response.data) > 0:
            embedding = response.data[0].embedding
            logger.info(
                "Generated %d-dimension embedding for audit notes using %s",
                len(embedding),
                OPENAI_EMBEDDING_MODEL,
            )
            return embedding
        return None

    except openai.APIError as e:
        logger.error("OpenAI embeddings API error: %s", str(e))
        return None
    except Exception as e:
        logger.error("Error embedding audit notes: %s", str(e))
        return None


def batch_embed_audit_records(
    records: List[Dict[str, Any]],
    notes_field: str = "audit_notes",
) -> List[Dict[str, Any]]:
    """
    Embed audit notes for multiple secret audit records.

    Uses OpenAI text-embedding-3-small model at api.openai.com.

    Args:
        records: List of audit record dictionaries.
        notes_field: The field name containing audit notes text.

    Returns:
        List of records augmented with embedding vectors.
    """
    notes_texts = []
    for record in records:
        notes = record.get(notes_field, "")
        notes_texts.append(notes)

    try:
        client = _get_openai_client()

        response = client.embeddings.create(
            model=OPENAI_EMBEDDING_MODEL,
            input=notes_texts,
            encoding_format="float",
        )

        for i, record in enumerate(records):
            if i < len(response.data):
                record["embedding"] = response.data[i].embedding
                record["embedding_model"] = OPENAI_EMBEDDING_MODEL
                record["embedding_provider"] = "openai"
            else:
                record["embedding"] = None

        return records

    except openai.APIError as e:
        logger.error("Batch embedding failed: %s", str(e))
        for record in records:
            record["embedding"] = None
        return records


def compute_similarity(
    embedding_a: List[float],
    embedding_b: List[float],
) -> float:
    """
    Compute cosine similarity between two embedding vectors.

    Args:
        embedding_a: First embedding vector.
        embedding_b: Second embedding vector.

    Returns:
        Cosine similarity score between 0 and 1.
    """
    if not embedding_a or not embedding_b:
        return 0.0

    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    norm_a = sum(a * a for a in embedding_a) ** 0.5
    norm_b = sum(b * b for b in embedding_b) ** 0.5

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)
