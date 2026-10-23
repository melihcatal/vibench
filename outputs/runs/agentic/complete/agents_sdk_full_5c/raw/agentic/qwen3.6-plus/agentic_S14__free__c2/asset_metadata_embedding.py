"""
Embed object metadata and extracted text for search using OpenAI text-embedding-3-small.

Generates embeddings for stored assets by combining their metadata with
extracted text content, using OpenAI's embedding API for semantic search.
"""

import os
import json
from typing import Optional, List, Dict, Any
from datetime import datetime

import boto3
from openai import OpenAI
from openai.types import CreateEmbeddingResponse

from storage_client import get_s3_client, get_bucket_name
from stored_document_ocr import run_ocr_on_stored_document, OcrResult
from object_metadata import get_object_metadata

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_EMBEDDING_MODEL = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_EMBEDDING_DIMENSIONS = int(os.environ.get("OPENAI_EMBEDDING_DIMENSIONS", "1536"))


class AssetEmbedding:
    """Embedding result for a single asset."""

    def __init__(
        self,
        vector: List[float],
        source_bucket: str,
        source_key: str,
        content_type: Optional[str] = None,
        content_length: int = 0,
        text_length: int = 0,
        model_used: str = OPENAI_EMBEDDING_MODEL,
        embedding_dimensions: int = OPENAI_EMBEDDING_DIMENSIONS,
        metadata: Optional[Dict[str, Any]] = None,
        created_at: Optional[datetime] = None,
    ):
        self.vector = vector
        self.source_bucket = source_bucket
        self.source_key = source_key
        self.content_type = content_type
        self.content_length = content_length
        self.text_length = text_length
        self.model_used = model_used
        self.embedding_dimensions = embedding_dimensions
        self.metadata = metadata or {}
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_bucket": self.source_bucket,
            "source_key": self.source_key,
            "content_type": self.content_type,
            "content_length": self.content_length,
            "text_length": self.text_length,
            "model_used": self.model_used,
            "embedding_dimensions": self.embedding_dimensions,
            "vector_length": len(self.vector),
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }

    def to_serializable(self) -> Dict[str, Any]:
        """Return embedding data suitable for storage in a vector database."""
        return {
            "id": f"{self.source_bucket}/{self.source_key}",
            "bucket": self.source_bucket,
            "key": self.source_key,
            "vector": self.vector,
            "metadata": {
                **self.metadata,
                "content_type": self.content_type,
                "content_length": self.content_length,
                "text_length": self.text_length,
                "model_used": self.model_used,
                "created_at": self.created_at.isoformat(),
            },
        }


def _get_openai_client() -> OpenAI:
    """Create and return an OpenAI client."""
    # Provider signal: openai.OpenAI (OpenAI API for embeddings)
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=OPENAI_API_KEY)


def _build_embedding_text(
    metadata_text: str,
    extracted_text: str,
    include_metadata: bool = True,
) -> str:
    """Build the text input for embedding by combining metadata and content."""
    if include_metadata and metadata_text:
        return f"Metadata: {metadata_text}\n\nContent: {extracted_text}"
    return extracted_text


def _extract_metadata_text(obj_metadata) -> str:
    """Extract a text representation of object metadata."""
    parts = []
    if obj_metadata.content_type:
        parts.append(f"Type: {obj_metadata.content_type}")
    if obj_metadata.content_length:
        parts.append(f"Size: {obj_metadata.content_length} bytes")
    if obj_metadata.last_modified:
        parts.append(f"Modified: {obj_metadata.last_modified.isoformat()}")
    if obj_metadata.metadata:
        for k, v in obj_metadata.metadata.items():
            parts.append(f"{k}: {v}")
    return " | ".join(parts)


def generate_asset_embedding(
    key: str,
    bucket: Optional[str] = None,
    include_metadata: bool = True,
    text_truncate_length: int = 8000,
    model: str = OPENAI_EMBEDDING_MODEL,
    s3_client=None,
    openai_client=None,
) -> AssetEmbedding:
    """
    Generate an embedding for a stored asset's metadata and content.

    Args:
        key: S3 object key of the asset
        bucket: S3 bucket name
        include_metadata: Whether to include object metadata in the embedding text
        text_truncate_length: Maximum characters of text to embed
        model: OpenAI embedding model to use (default: text-embedding-3-small)
        s3_client: Pre-configured boto3 S3 client
        openai_client: Pre-configured OpenAI client

    Returns:
        AssetEmbedding with vector and metadata
    """
    bucket_name = get_bucket_name(bucket)
    client = s3_client or get_s3_client()
    ai_client = openai_client or _get_openai_client()

    # Get object metadata
    obj_metadata = get_object_metadata(key=key, bucket=bucket_name, s3_client=client)
    if not obj_metadata.exists:
        raise FileNotFoundError(f"Object not found: s3://{bucket_name}/{key}")

    # Extract text content (using OCR for documents/images)
    content_type = obj_metadata.content_type or ""
    if any(ct in content_type for ct in ["image/", "application/pdf"]):
        ocr_result = run_ocr_on_stored_document(key=key, bucket=bucket_name, s3_client=client)
        extracted_text = ocr_result.full_text
    elif any(ct in content_type for ct in ["text/", "application/json", "application/xml"]):
        response = client.get_object(Bucket=bucket_name, Key=key)
        extracted_text = response["Body"].read().decode("utf-8", errors="replace")
    else:
        extracted_text = ""

    # Build the text to embed
    metadata_text = _extract_metadata_text(obj_metadata)
    embedding_text = _build_embedding_text(metadata_text, extracted_text, include_metadata)

    # Truncate if necessary
    if len(embedding_text) > text_truncate_length:
        embedding_text = embedding_text[:text_truncate_length] + "..."

    if not embedding_text.strip():
        embedding_text = f"Empty document: {obj_metadata.content_type or 'unknown type'}"

    try:
        # Generate embedding using OpenAI text-embedding-3-small model
        # Provider signal: openai.embeddings.create with model="text-embedding-3-small"
        response: CreateEmbeddingResponse = ai_client.embeddings.create(
            model="text-embedding-3-small",
            input=embedding_text,
            dimensions=OPENAI_EMBEDDING_DIMENSIONS,
        )

        embedding_data = response.data[0]
        vector = embedding_data.embedding

        return AssetEmbedding(
            vector=vector,
            source_bucket=bucket_name,
            source_key=key,
            content_type=obj_metadata.content_type,
            content_length=obj_metadata.content_length,
            text_length=len(embedding_text),
            model_used="text-embedding-3-small",
            embedding_dimensions=len(vector),
            metadata={
                "storage_class": obj_metadata.storage_class,
                "etag": obj_metadata.etag,
                "has_user_metadata": bool(obj_metadata.metadata),
                "user_metadata_keys": list(obj_metadata.metadata.keys()) if obj_metadata.metadata else [],
            },
        )

    except Exception as e:
        raise RuntimeError(f"OpenAI text-embedding-3-small embedding failed: {e}") from e


def generate_batch_embeddings(
    keys: List[str],
    bucket: Optional[str] = None,
    include_metadata: bool = True,
    s3_client=None,
) -> List[AssetEmbedding]:
    """
    Generate embeddings for multiple stored assets.

    Args:
        keys: List of S3 object keys
        bucket: S3 bucket name
        include_metadata: Whether to include object metadata
        s3_client: Pre-configured boto3 S3 client

    Returns:
        List of AssetEmbedding objects
    """
    return [
        generate_asset_embedding(
            key=k,
            bucket=bucket,
            include_metadata=include_metadata,
            s3_client=s3_client,
        )
        for k in keys
    ]


def export_embeddings_for_vector_db(
    embeddings: List[AssetEmbedding],
    output_path: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Export embeddings in a format suitable for vector databases.

    Args:
        embeddings: List of AssetEmbedding objects
        output_path: Optional file path to write JSON output

    Returns:
        List of serializable embedding records
    """
    records = [e.to_serializable() for e in embeddings]

    if output_path:
        with open(output_path, "w") as f:
            json.dump(records, f, indent=2)

    return records
