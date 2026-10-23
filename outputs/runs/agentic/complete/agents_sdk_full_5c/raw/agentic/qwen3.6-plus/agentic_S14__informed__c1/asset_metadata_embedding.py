"""
Embed object metadata and extracted text for search using OpenAI Embeddings.

Uses the OpenAI Python SDK (openai) to generate vector embeddings via the
OpenAI embeddings API (text-embedding-3-small, text-embedding-3-large).
Authentication via OPENAI_API_KEY environment variable.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
from dataclasses import dataclass, field
from typing import Any, Optional

import openai

logger = logging.getLogger(__name__)

# Provider-identifying environment variable for OpenAI
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"

# OpenAI embedding model identifiers
OPENAI_EMBEDDING_MODEL_3_SMALL = "text-embedding-3-small"
OPENAI_EMBEDDING_MODEL_3_LARGE = "text-embedding-3-large"
OPENAI_EMBEDDING_MODEL_ADA_002 = "text-embedding-ada-002"

DEFAULT_EMBEDDING_MODEL = OPENAI_EMBEDDING_MODEL_3_SMALL


@dataclass
class EmbeddingResult:
    """Holds an embedding vector and its associated metadata."""
    vector: list[float] = field(default_factory=list)
    model: str = ""
    input_text_hash: str = ""
    dimensions: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


def create_openai_client(
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
) -> openai.OpenAI:
    """
    Create an OpenAI API client using the Python SDK.

    Args:
        api_key: OpenAI API key. Falls back to OPENAI_API_KEY env var.
        organization: Optional OpenAI organization ID.

    Returns:
        Configured openai.OpenAI client instance.
    """
    key = api_key or os.environ.get(OPENAI_API_KEY_ENV)
    if not key:
        raise ValueError(
            f"OpenAI API key not provided. Set the {OPENAI_API_KEY_ENV} environment variable."
        )
    kwargs: dict[str, str] = {"api_key": key}
    if organization:
        kwargs["organization"] = organization
    client = openai.OpenAI(**kwargs)
    logger.debug("Created OpenAI client for embeddings")
    return client


def generate_embedding(
    text: str,
    *,
    model: str = DEFAULT_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
    client: Optional[openai.OpenAI] = None,
) -> EmbeddingResult:
    """
    Generate an embedding vector for a single text input using OpenAI.

    Args:
        text: Text to embed.
        model: OpenAI embedding model ID.
        dimensions: Optional output dimensionality (supported by text-embedding-3-*).
        api_key: Optional OpenAI API key.
        client: Optional pre-created openai.OpenAI client.

    Returns:
        EmbeddingResult with the vector and metadata.
    """
    if client is None:
        client = create_openai_client(api_key=api_key)

    text_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

    kwargs: dict[str, Any] = {
        "input": text,
        "model": model,
    }
    if dimensions is not None:
        kwargs["dimensions"] = dimensions

    try:
        response = client.embeddings.create(**kwargs)
    except openai.APIError as exc:
        logger.error("OpenAI embedding generation failed: %s", exc)
        raise

    embedding_data = response.data[0]
    vector = embedding_data.embedding

    result = EmbeddingResult(
        vector=vector,
        model=model,
        input_text_hash=text_hash,
        dimensions=len(vector),
    )
    logger.info(
        "Generated embedding with OpenAI %s: %d dimensions (hash=%s)",
        model,
        len(vector),
        text_hash,
    )
    return result


def generate_batch_embeddings(
    texts: list[str],
    *,
    model: str = DEFAULT_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
    client: Optional[openai.OpenAI] = None,
) -> list[EmbeddingResult]:
    """
    Generate embedding vectors for multiple texts in a single OpenAI API call.

    Args:
        texts: List of texts to embed (up to OpenAI batch limit).
        model: OpenAI embedding model ID.
        dimensions: Optional output dimensionality.
        api_key: Optional OpenAI API key.
        client: Optional pre-created openai.OpenAI client.

    Returns:
        List of EmbeddingResult objects, one per input text.
    """
    if client is None:
        client = create_openai_client(api_key=api_key)

    if not texts:
        return []

    kwargs: dict[str, Any] = {
        "input": texts,
        "model": model,
    }
    if dimensions is not None:
        kwargs["dimensions"] = dimensions

    try:
        response = client.embeddings.create(**kwargs)
    except openai.APIError as exc:
        logger.error("OpenAI batch embedding generation failed: %s", exc)
        raise

    results = []
    for i, embedding_data in enumerate(response.data):
        text_hash = hashlib.sha256(texts[i].encode("utf-8")).hexdigest()[:16]
        results.append(
            EmbeddingResult(
                vector=embedding_data.embedding,
                model=model,
                input_text_hash=text_hash,
                dimensions=len(embedding_data.embedding),
            )
        )

    logger.info(
        "Generated %d embeddings with OpenAI %s",
        len(results),
        model,
    )
    return results


def embed_object_metadata_and_text(
    object_key: str,
    bucket: str,
    extracted_text: str,
    metadata: Optional[dict[str, str]] = None,
    *,
    model: str = DEFAULT_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
    client: Optional[openai.OpenAI] = None,
) -> list[EmbeddingResult]:
    """
    Create embeddings for both object metadata and extracted text content.

    Generates separate embeddings for:
    1. A combined metadata string (bucket, key, content-type, custom metadata)
    2. The full extracted text content
    3. Individual metadata fields (for field-level search)

    Args:
        object_key: S3 object key.
        bucket: S3 bucket name.
        extracted_text: OCR or extracted text from the object.
        metadata: Optional dict of object metadata key-value pairs.
        model: OpenAI embedding model ID.
        dimensions: Optional output dimensionality.
        api_key: Optional OpenAI API key.
        client: Optional pre-created openai.OpenAI client.

    Returns:
        List of EmbeddingResult objects for metadata, text, and individual fields.
    """
    if client is None:
        client = create_openai_client(api_key=api_key)

    # Build combined metadata string
    meta_parts = [
        f"bucket: {bucket}",
        f"key: {object_key}",
    ]
    if metadata:
        for k, v in sorted(metadata.items()):
            meta_parts.append(f"{k}: {v}")
    metadata_str = " | ".join(meta_parts)

    # Collect all texts to embed
    texts_to_embed = [
        metadata_str,  # Combined metadata
        extracted_text,  # Full text content
    ]

    # Add individual metadata fields
    if metadata:
        for k, v in sorted(metadata.items()):
            texts_to_embed.append(f"{k}: {v}")

    # Generate batch embeddings
    embeddings = generate_batch_embeddings(
        texts_to_embed,
        model=model,
        dimensions=dimensions,
        client=client,
    )

    # Tag embeddings with their purpose
    if len(embeddings) >= 2:
        embeddings[0].metadata = {
            "type": "combined_metadata",
            "object_key": object_key,
            "bucket": bucket,
        }
        embeddings[1].metadata = {
            "type": "extracted_text",
            "object_key": object_key,
            "bucket": bucket,
            "text_length": len(extracted_text),
        }

    for i, meta_kv in enumerate(sorted((metadata or {}).items())):
        idx = 2 + i
        if idx < len(embeddings):
            embeddings[idx].metadata = {
                "type": "metadata_field",
                "field_name": meta_kv[0],
                "object_key": object_key,
                "bucket": bucket,
            }

    logger.info(
        "Embedded object s3://%s/%s: %d vectors (%d text chars, %d metadata fields)",
        bucket,
        object_key,
        len(embeddings),
        len(extracted_text),
        len(metadata or {}),
    )
    return embeddings


def vector_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """
    Compute cosine similarity between two embedding vectors.

    Args:
        vec_a: First embedding vector.
        vec_b: Second embedding vector.

    Returns:
        Cosine similarity score in [-1, 1].
    """
    import math

    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must have the same dimensions.")

    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)
