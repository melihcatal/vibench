"""
asset_metadata_embedding.py — Embed object metadata and extracted text for search.

Concrete provider: OpenAI Embeddings API via the `openai` SDK.
Provider signals:
  - openai import and OpenAI client
  - text-embedding-3-small / text-embedding-3-large model identifiers
  - OPENAI_API_KEY environment variable
"""

import os
import json
from typing import Any, Dict, List, Optional
from openai import OpenAI, APIError


def embed_object_metadata_and_text(
    object_metadata: Dict[str, Any],
    extracted_text: str,
    model: str = "text-embedding-3-small",
    metadata_weight: float = 0.3,
) -> Dict:
    """
    Generate embeddings for both object metadata and extracted text
    using OpenAI's Embeddings API.

    Combines metadata fields and text content into a searchable vector
    representation. Metadata and text are embedded separately and can
    be combined with weighting.

    Parameters
    ----------
    object_metadata : dict
        Object metadata (e.g., filename, content type, size, tags, custom fields).
    extracted_text : str
        Text extracted from the stored asset (e.g., OCR output).
    model : str
        OpenAI embedding model (default: text-embedding-3-small).
        Options: text-embedding-3-small (1536-dim), text-embedding-3-large (3072-dim).
    metadata_weight : float
        Weight for metadata portion in combined embedding (0.0–1.0).

    Returns
    -------
    dict
        Embedding result with vector, metadata summary, and model info.

    Raises
    ------
    APIError
        When the OpenAI API call fails.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    # Serialize metadata into a text representation for embedding
    metadata_text = _serialize_metadata(object_metadata)

    # Embed metadata and extracted text separately
    metadata_embedding = _get_embedding(client, metadata_text, model)
    text_embedding = _get_embedding(client, extracted_text, model)

    # Create combined weighted embedding
    combined_embedding = _combine_embeddings(
        metadata_embedding, text_embedding, metadata_weight
    )

    return {
        "embedding": combined_embedding,
        "metadata_embedding": metadata_embedding,
        "text_embedding": text_embedding,
        "dimension": len(combined_embedding),
        "model": model,
        "service": "OpenAI Embeddings API",
        "metadata_weight": metadata_weight,
        "metadata_fields_embedded": list(object_metadata.keys()),
        "text_length": len(extracted_text),
    }


def embed_batch_texts(
    texts: List[str],
    model: str = "text-embedding-3-small",
    max_batch_size: int = 100,
) -> Dict:
    """
    Embed multiple text items in a batch using OpenAI Embeddings API.

    Parameters
    ----------
    texts : list[str]
        List of text strings to embed.
    model : str
        OpenAI embedding model.
    max_batch_size : int
        Maximum items per API call (OpenAI limit is 2048).

    Returns
    -------
    dict
        Batch embedding result with all vectors and per-item metadata.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    all_embeddings = []
    for i in range(0, len(texts), max_batch_size):
        batch = texts[i:i + max_batch_size]
        response = client.embeddings.create(
            input=batch,
            model=model,
        )
        for item in response.data:
            all_embeddings.append({
                "index": item.index,
                "embedding": item.embedding,
                "original_text": batch[item.index] if item.index < len(batch) else "",
            })

    return {
        "embeddings": all_embeddings,
        "model": model,
        "service": "OpenAI Embeddings API",
        "total_items": len(all_embeddings),
        "dimension": len(all_embeddings[0]["embedding"]) if all_embeddings else 0,
    }


def _serialize_metadata(metadata: Dict[str, Any]) -> str:
    """Convert metadata dict into a text string suitable for embedding."""
    parts = []
    for key, value in metadata.items():
        if isinstance(value, (dict, list)):
            parts.append(f"{key}: {json.dumps(value)}")
        else:
            parts.append(f"{key}: {value}")
    return " | ".join(parts)


def _get_embedding(client: OpenAI, text: str, model: str) -> List[float]:
    """Get a single embedding vector from OpenAI."""
    if not text.strip():
        # Return zero vector for empty text
        if "large" in model:
            return [0.0] * 3072
        return [0.0] * 1536

    response = client.embeddings.create(
        input=text,
        model=model,
    )
    return response.data[0].embedding


def _combine_embeddings(
    embedding_a: List[float],
    embedding_b: List[float],
    weight_a: float,
) -> List[float]:
    """Combine two embeddings with weighted averaging."""
    weight_b = 1.0 - weight_a
    min_len = min(len(embedding_a), len(embedding_b))

    combined = []
    for i in range(min_len):
        combined.append(
            weight_a * embedding_a[i] + weight_b * embedding_b[i]
        )

    return combined
