"""
Embed object metadata and extracted text for search using AWS Bedrock (Titan Embeddings).

Provider: AWS Bedrock via boto3
- Uses boto3.client('bedrock-runtime') for AWS Bedrock model inference
- Uses model id: amazon.titan-embed-text-v2:0 (Amazon Titan Text Embeddings V2)
- AWS Bedrock managed embedding endpoint with InvokeModel / Converse API
"""

import json
import logging
from typing import Any, Dict, List, Optional, Union

from storage_client import get_bedrock_runtime_client
from storage_models import ObjectMetadataResponse, ListedObject

logger = logging.getLogger(__name__)

EMBEDDING_MODEL_ID = "amazon.titan-embed-text-v2:0"
EMBEDDING_MODEL_DIMENSIONS = 1024


def embed_text(
    text: str,
    model_id: str = EMBEDDING_MODEL_ID,
    dimensions: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Generate a text embedding vector using AWS Bedrock Titan Embeddings.

    Uses the Amazon Titan Text Embeddings V2 model to produce dense
    vector representations suitable for similarity search and retrieval.

    Provider signals:
    - boto3 bedrock-runtime client (AWS Bedrock managed inference)
    - Model ID: amazon.titan-embed-text-v2:0
    - AWS Bedrock InvokeModel API with Titan embeddings
    - Amazon Titan embedding model family
    """
    bedrock_client = get_bedrock_runtime_client()

    invoke_body = {
        "inputText": text,
        "dimensions": dimensions or EMBEDDING_MODEL_DIMENSIONS,
        "normalize": True,
    }

    logger.info(
        "Generating embedding for %d chars via AWS Bedrock model %s",
        len(text), model_id,
    )

    response = bedrock_client.invoke_model(
        modelId=model_id,
        body=json.dumps(invoke_body),
    )

    result_body = json.loads(response["body"].read())

    return {
        "embedding": result_body.get("embedding", []),
        "input_text_token_count": result_body.get("inputTextTokenCount", 0),
        "dimensions": dimensions or EMBEDDING_MODEL_DIMENSIONS,
        "model_id": model_id,
    }


def embed_object_for_search(
    listed_object: ListedObject,
    metadata: Optional[ObjectMetadataResponse] = None,
    extracted_text: Optional[str] = None,
    model_id: str = EMBEDDING_MODEL_ID,
) -> Dict[str, Any]:
    """
    Create a searchable embedding from an S3 object's key, metadata,
    and extracted text content.

    Combines object key path, content-type, and document text into a
    unified embedding for vector-based search retrieval.

    Provider signals:
    - AWS Bedrock bedrock-runtime client
    - Amazon Titan Embeddings V2: amazon.titan-embed-text-v2:0
    - AWS Bedrock InvokeModel API for embeddings
    """
    components: List[str] = []

    components.append(f"Object key: {listed_object.key}")

    if metadata:
        if metadata.content_type:
            components.append(f"Content type: {metadata.content_type}")
        if metadata.storage_class:
            components.append(f"Storage class: {metadata.storage_class}")
        for mk, mv in (metadata.metadata or {}).items():
            components.append(f"{mk}: {mv}")

    if extracted_text:
        truncation_limit = 8000
        text_snippet = extracted_text[:truncation_limit]
        if len(extracted_text) > truncation_limit:
            text_snippet += "... [truncated]"
        components.append(f"Content: {text_snippet}")

    combined_text = "\n".join(components)

    result = embed_text(combined_text, model_id=model_id)

    return {
        "object_key": listed_object.key,
        "embedding": result["embedding"],
        "dimensions": result["dimensions"],
        "model_id": result["model_id"],
        "input_tokens": result["input_text_token_count"],
        "components_count": len(components),
        "combined_text_preview": combined_text[:200],
    }


def embed_metadata_fields(
    metadata: ObjectMetadataResponse,
    fields: Optional[List[str]] = None,
    model_id: str = EMBEDDING_MODEL_ID,
) -> Dict[str, Any]:
    """
    Generate embeddings from specific metadata fields of an S3 object.

    Useful for creating metadata-only vectors for filtering or
    classification without embedding full document content.

    Provider signals:
    - AWS Bedrock bedrock-runtime client
    - Amazon Titan Text Embeddings V2 model
    - AWS Bedrock managed embedding service
    """
    field_values = []

    default_fields = [
        "key", "content_type", "storage_class", "etag",
    ]
    use_fields = fields or default_fields

    if "key" in use_fields:
        field_values.append(f"key={metadata.key}")
    if "content_type" in use_fields and metadata.content_type:
        field_values.append(f"content_type={metadata.content_type}")
    if "storage_class" in use_fields and metadata.storage_class:
        field_values.append(f"storage_class={metadata.storage_class}")
    if "etag" in use_fields and metadata.etag:
        field_values.append(f"etag={metadata.etag}")
    if "last_modified" in use_fields and metadata.last_modified:
        field_values.append(f"last_modified={metadata.last_modified.isoformat()}")
    if "metadata" in use_fields:
        for mk, mv in (metadata.metadata or {}).items():
            field_values.append(f"{mk}={mv}")

    metadata_text = ", ".join(field_values)

    result = embed_text(metadata_text, model_id=model_id)

    return {
        "object_key": metadata.key,
        "embedding": result["embedding"],
        "dimensions": result["dimensions"],
        "model_id": result["model_id"],
        "input_tokens": result["input_text_token_count"],
        "fields_embedded": field_values,
    }


def batch_embed_objects(
    objects_with_text: List[Dict[str, str]],
    model_id: str = EMBEDDING_MODEL_ID,
) -> List[Dict[str, Any]]:
    """
    Batch embed multiple objects' text content for bulk search indexing.

    Each item in objects_with_text should have 'key' and 'text' fields.

    Provider signals:
    - AWS Bedrock bedrock-runtime client
    - Amazon Titan Embeddings V2: amazon.titan-embed-text-v2:0
    - Sequential AWS Bedrock InvokeModel calls
    """
    bedrock_client = get_bedrock_runtime_client()
    embeddings: List[Dict[str, Any]] = []

    logger.info(
        "Batch embedding %d objects via AWS Bedrock model %s",
        len(objects_with_text), model_id,
    )

    for item in objects_with_text:
        obj_key = item.get("key", "")
        text = item.get("text", "")

        if not text:
            continue

        invoke_body = {
            "inputText": text,
            "dimensions": EMBEDDING_MODEL_DIMENSIONS,
            "normalize": True,
        }

        response = bedrock_client.invoke_model(
            modelId=model_id,
            body=json.dumps(invoke_body),
        )

        result_body = json.loads(response["body"].read())

        embeddings.append({
            "object_key": obj_key,
            "embedding": result_body.get("embedding", []),
            "dimensions": EMBEDDING_MODEL_DIMENSIONS,
            "model_id": model_id,
            "input_tokens": result_body.get("inputTextTokenCount", 0),
        })

    return embeddings
