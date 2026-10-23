from __future__ import annotations

import json
from typing import Optional

from storage_client import (
    get_bedrock_runtime_client,
    get_object_metadata,
    get_object_content,
    get_s3_client,
)
from storage_models import (
    EmbeddingRequest,
    EmbeddingResponse,
    MetadataRequest,
    normalize_embedding_response,
)

TITAN_EMBEDDING_MODEL_ID = "amazon.titan-embed-text-v2:0"


def embed_object_metadata_and_text(
    bucket: str,
    key: str,
    version_id: Optional[str] = None,
    bedrock_client=None,
    s3_client=None,
) -> EmbeddingResponse:
    if s3_client is None:
        s3_client = get_s3_client()
    if bedrock_client is None:
        bedrock_client = get_bedrock_runtime_client()

    metadata_request = MetadataRequest(
        bucket=bucket,
        key=key,
        version_id=version_id,
    )
    metadata = get_object_metadata(metadata_request, client=s3_client)

    document_bytes = get_object_content(bucket, key, version_id, client=s3_client)
    text_content = document_bytes.decode("utf-8", errors="replace")

    metadata_str = json.dumps(
        {
            "content_type": metadata.content_type,
            "content_length": metadata.content_length,
            "storage_class": metadata.storage_class,
            "last_modified": metadata.last_modified.isoformat()
            if metadata.last_modified
            else None,
            "custom_metadata": metadata.metadata,
        }
    )

    combined_text = f"Metadata: {metadata_str}\n\nContent: {text_content}"

    request = EmbeddingRequest(
        text=combined_text,
        metadata=metadata.metadata,
    )

    body = json.dumps(
        {
            "inputText": combined_text,
            "dimensions": 1024,
            "normalize": True,
        }
    )

    response = bedrock_client.invoke_model(
        modelId=TITAN_EMBEDDING_MODEL_ID,
        body=body,
        contentType="application/json",
        accept="application/json",
    )

    return normalize_embedding_response(response, TITAN_EMBEDDING_MODEL_ID)


def embed_text_for_search(
    text: str,
    dimensions: int = 1024,
    normalize: bool = True,
    bedrock_client=None,
) -> EmbeddingResponse:
    if bedrock_client is None:
        bedrock_client = get_bedrock_runtime_client()

    request = EmbeddingRequest(text=text)

    body = json.dumps(
        {
            "inputText": text,
            "dimensions": dimensions,
            "normalize": normalize,
        }
    )

    response = bedrock_client.invoke_model(
        modelId=TITAN_EMBEDDING_MODEL_ID,
        body=body,
        contentType="application/json",
        accept="application/json",
    )

    return normalize_embedding_response(response, TITAN_EMBEDDING_MODEL_ID)


def embed_metadata_for_search(
    bucket: str,
    key: str,
    version_id: Optional[str] = None,
    bedrock_client=None,
    s3_client=None,
) -> EmbeddingResponse:
    if s3_client is None:
        s3_client = get_s3_client()
    if bedrock_client is None:
        bedrock_client = get_bedrock_runtime_client()

    metadata_request = MetadataRequest(
        bucket=bucket,
        key=key,
        version_id=version_id,
    )
    metadata = get_object_metadata(metadata_request, client=s3_client)

    metadata_payload = json.dumps(
        {
            "bucket": bucket,
            "key": key,
            "content_type": metadata.content_type,
            "content_length": metadata.content_length,
            "storage_class": metadata.storage_class,
            "last_modified": metadata.last_modified.isoformat()
            if metadata.last_modified
            else None,
            "etag": metadata.etag,
            "custom_metadata": metadata.metadata,
        }
    )

    request = EmbeddingRequest(
        text=metadata_payload,
        metadata=metadata.metadata,
    )

    body = json.dumps(
        {
            "inputText": metadata_payload,
            "dimensions": 1024,
            "normalize": True,
        }
    )

    response = bedrock_client.invoke_model(
        modelId=TITAN_EMBEDDING_MODEL_ID,
        body=body,
        contentType="application/json",
        accept="application/json",
    )

    return normalize_embedding_response(response, TITAN_EMBEDDING_MODEL_ID)
