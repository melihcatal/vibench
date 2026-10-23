"""
Embed object metadata and extracted text for search using OpenAI embeddings.

Uses openai SDK for OpenAI Embeddings API (service=OpenAI embeddings).
Model: text-embedding-3-small (with text-embedding-3-large and text-embedding-ada-002 as alternatives).
Environment variable: OPENAI_API_KEY
"""

import json
from typing import Any, Dict, List, Optional

import openai

from storage_models import ObjectMetadataResponse
from object_metadata import get_object_metadata
from stored_document_ocr import run_ocr_on_stored_document


DEFAULT_MODEL = "text-embedding-3-small"

SUPPORTED_MODELS = [
    "text-embedding-3-small",
    "text-embedding-3-large",
    "text-embedding-ada-002",
]


def _get_openai_client() -> openai.OpenAI:
    """
    Create an OpenAI API client using the OPENAI_API_KEY environment variable.

    Returns:
        openai.OpenAI: Authenticated client for OpenAI Embeddings API.

    Raises:
        ValueError: If OPENAI_API_KEY is not set.
    """
    import os

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable must be set for OpenAI Embeddings API access"
        )
    return openai.OpenAI(api_key=api_key)


def _build_embedding_input(
    metadata: Optional[ObjectMetadataResponse],
    extracted_text: Optional[str],
    additional_fields: Optional[Dict[str, Any]],
) -> str:
    """
    Build a normalized text string for embedding from metadata and extracted text.

    Combines object metadata, document content, and any additional fields
    into a structured text format suitable for semantic search.

    Args:
        metadata: Object metadata from S3 head_object.
        extracted_text: OCR-extracted text content.
        additional_fields: Extra key-value pairs to include.

    Returns:
        str: Combined text representation for embedding.
    """
    parts = []

    if metadata:
        meta_parts = []
        if metadata.object_key:
            meta_parts.append(f"object_key: {metadata.object_key}")
        if metadata.bucket:
            meta_parts.append(f"bucket: {metadata.bucket}")
        if metadata.content_type:
            meta_parts.append(f"content_type: {metadata.content_type}")
        if metadata.content_length is not None:
            meta_parts.append(f"content_length: {metadata.content_length}")
        if metadata.storage_class:
            meta_parts.append(f"storage_class: {metadata.storage_class}")
        if metadata.last_modified:
            meta_parts.append(f"last_modified: {metadata.last_modified.isoformat()}")
        if metadata.metadata:
            for k, v in metadata.metadata.items():
                meta_parts.append(f"metadata.{k}: {v}")
        if meta_parts:
            parts.append("Document Metadata:\n" + "\n".join(meta_parts))

    if extracted_text and extracted_text.strip():
        parts.append("Document Content:\n" + extracted_text.strip())

    if additional_fields:
        extra_parts = []
        for k, v in additional_fields.items():
            extra_parts.append(f"{k}: {v}")
        if extra_parts:
            parts.append("Additional Fields:\n" + "\n".join(extra_parts))

    return "\n\n".join(parts)


def embed_asset_metadata_and_text(
    bucket: str,
    object_key: str,
    prefix: Optional[str] = None,
    additional_fields: Optional[Dict[str, Any]] = None,
    include_ocr: bool = True,
    model: str = DEFAULT_MODEL,
    dimensions: Optional[int] = None,
) -> Dict:
    """
    Generate embeddings for an S3 object by combining its metadata and extracted text.

    Retrieves object metadata from S3, optionally runs OCR on the document,
    then generates a combined embedding using OpenAI's text-embedding-3-small model.

    Args:
        bucket: The S3 bucket containing the object.
        object_key: The S3 object key.
        prefix: Optional prefix for the S3 object key.
        additional_fields: Extra metadata fields to include in the embedding input.
        include_ocr: If True, run OCR and include extracted text in the embedding.
        model: OpenAI embedding model identifier (default: text-embedding-3-small).
        dimensions: Optional output dimension count (supported for text-embedding-3-* models).

    Returns:
        dict with keys:
            - embedding: List of float values representing the embedding vector
            - model: The embedding model used
            - input_text_length: Length of the text that was embedded
            - metadata: Object metadata that was included
            - ocr_included: Whether OCR text was included
            - dimensions: Actual dimension count of the returned embedding

    Raises:
        FileNotFoundError: If the S3 object does not exist.
        openai.APIError: On OpenAI API errors.
    """
    if model not in SUPPORTED_MODELS:
        model = DEFAULT_MODEL

    metadata = get_object_metadata(bucket, object_key, prefix=prefix)
    if metadata is None:
        raise FileNotFoundError(
            f"Object s3://{bucket}/{object_key} not found"
        )

    extracted_text = None
    if include_ocr:
        try:
            ocr_result = run_ocr_on_stored_document(bucket, object_key, prefix=prefix)
            extracted_text = ocr_result["text"]
        except Exception:
            extracted_text = None

    embedding_input = _build_embedding_input(metadata, extracted_text, additional_fields)

    if not embedding_input.strip():
        return {
            "embedding": [],
            "model": model,
            "input_text_length": 0,
            "metadata": {
                "object_key": metadata.object_key,
                "bucket": metadata.bucket,
                "content_type": metadata.content_type,
                "content_length": metadata.content_length,
            },
            "ocr_included": include_ocr and extracted_text is not None,
            "dimensions": 0,
        }

    client = _get_openai_client()

    kwargs = {
        "model": model,
        "input": embedding_input,
    }

    if dimensions is not None and model in ("text-embedding-3-small", "text-embedding-3-large"):
        kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**kwargs)

    embedding_vector = response.data[0].embedding

    return {
        "embedding": embedding_vector,
        "model": model,
        "input_text_length": len(embedding_input),
        "metadata": {
            "object_key": metadata.object_key,
            "bucket": metadata.bucket,
            "content_type": metadata.content_type,
            "content_length": metadata.content_length,
            "storage_class": metadata.storage_class,
            "last_modified": metadata.last_modified.isoformat() if metadata.last_modified else None,
            "user_metadata": metadata.metadata,
        },
        "ocr_included": include_ocr and extracted_text is not None,
        "dimensions": len(embedding_vector),
    }


def embed_batch(
    texts: List[str],
    model: str = DEFAULT_MODEL,
    dimensions: Optional[int] = None,
) -> List[List[float]]:
    """
    Generate embeddings for a batch of text strings.

    Args:
        texts: List of text strings to embed.
        model: OpenAI embedding model identifier.
        dimensions: Optional output dimension count.

    Returns:
        List of embedding vectors, one per input text.
    """
    if not texts:
        return []

    client = _get_openai_client()

    kwargs = {
        "model": model,
        "input": texts,
    }

    if dimensions is not None and model in ("text-embedding-3-small", "text-embedding-3-large"):
        kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**kwargs)

    return [data.embedding for data in response.data]


def compute_similarity(embedding_a: List[float], embedding_b: List[float]) -> float:
    """
    Compute cosine similarity between two embedding vectors.

    Args:
        embedding_a: First embedding vector.
        embedding_b: Second embedding vector.

    Returns:
        float: Cosine similarity score between 0 and 1.
    """
    import math

    if not embedding_a or not embedding_b:
        return 0.0

    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    norm_a = math.sqrt(sum(a * a for a in embedding_a))
    norm_b = math.sqrt(sum(b * b for b in embedding_b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)
