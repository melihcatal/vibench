import boto3
import os
import json
from typing import Dict, List, Any
from botocore.exceptions import ClientError


def embed_object_metadata_and_text(
    metadata: Dict[str, Any],
    text: str = "",
    bedrock_client=None,
    model_id: str = "amazon.titan-embed-text-v1",
) -> dict:
    """
    Embed object metadata and extracted text for search using Amazon Titan Embeddings.

    Args:
        metadata: Object metadata dictionary
        text: Extracted text content (optional)
        bedrock_client: Optional Bedrock Runtime client (will create if not provided)
        model_id: Bedrock embeddings model ID (default: 'amazon.titan-embed-text-v1')

    Returns:
        Dictionary with embedding results
    """
    # Create Bedrock Runtime client if not provided
    if bedrock_client is None:
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        aws_region = os.getenv("AWS_REGION", "us-east-1")

        if not aws_access_key_id or not aws_secret_access_key:
            raise ValueError(
                "AWS credentials not found in environment. "
                "Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY."
            )

        bedrock_client = boto3.client(
            "bedrock-runtime",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region,
        )

    try:
        # Prepare text for embedding
        embedding_text = prepare_text_for_embedding(metadata, text)

        # Prepare request body for Titan embeddings model
        body = json.dumps({"inputText": embedding_text})

        # Call Amazon Bedrock for embeddings
        response = bedrock_client.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json",
        )

        # Parse response
        response_body = json.loads(response["body"].read())

        # Extract embedding vector
        embedding = response_body.get("embedding", [])

        # Get embedding dimensions
        dimensions = len(embedding)

        return {
            "success": True,
            "embedding": embedding,
            "dimensions": dimensions,
            "model_id": model_id,
            "input_text_length": len(embedding_text),
            "embedding_text": embedding_text,
            "metadata_keys": list(metadata.keys()) if metadata else [],
            "has_text_content": bool(text),
        }

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "Unknown")
        return {
            "success": False,
            "error": str(e),
            "error_code": error_code,
            "model_id": model_id,
            "metadata_keys": list(metadata.keys()) if metadata else [],
            "has_text_content": bool(text),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "model_id": model_id,
            "metadata_keys": list(metadata.keys()) if metadata else [],
            "has_text_content": bool(text),
        }


def prepare_text_for_embedding(metadata: Dict[str, Any], text: str = "") -> str:
    """
    Prepare combined text from metadata and content for embedding.

    Args:
        metadata: Object metadata dictionary
        text: Extracted text content

    Returns:
        Combined text string for embedding
    """
    parts = []

    # Add key metadata fields
    if metadata:
        # Add bucket and key if present
        if "bucket" in metadata:
            parts.append(f"Bucket: {metadata['bucket']}")
        if "key" in metadata:
            parts.append(f"Key: {metadata['key']}")

        # Add content type if present
        if "content_type" in metadata and metadata["content_type"]:
            parts.append(f"Content type: {metadata['content_type']}")

        # Add size if present
        if "size" in metadata:
            parts.append(f"Size: {metadata['size']} bytes")

        # Add storage class if present
        if "storage_class" in metadata and metadata["storage_class"]:
            parts.append(f"Storage class: {metadata['storage_class']}")

        # Add custom metadata
        if "metadata" in metadata and isinstance(metadata["metadata"], dict):
            for key, value in metadata["metadata"].items():
                parts.append(f"{key}: {value}")

    # Add extracted text content
    if text:
        # Truncate text if too long (Titan embeddings have token limits)
        max_text_length = 8000  # Conservative limit
        if len(text) > max_text_length:
            text = text[:max_text_length] + "... [truncated]"
        parts.append(f"Content: {text}")

    return "\n".join(parts)


def embed_asset_with_ocr(
    metadata_result: dict,
    ocr_result: dict,
    model_id: str = "amazon.titan-embed-text-v1",
) -> dict:
    """
    Embed asset metadata with OCR extracted text.

    Args:
        metadata_result: Metadata result from object_metadata.py
        ocr_result: OCR result from stored_document_ocr.py
        model_id: Bedrock model ID (default: 'amazon.titan-embed-text-v1')

    Returns:
        Dictionary with embedding results
    """
    if not metadata_result.get("success", False):
        return {
            "success": False,
            "error": "Metadata result was not successful",
            "metadata_result": metadata_result,
        }

    text_content = ""
    if ocr_result.get("success", False):
        text_content = ocr_result.get("full_text", "")

    # Embed metadata and text
    embedding_result = embed_object_metadata_and_text(
        metadata=metadata_result, text=text_content, model_id=model_id
    )

    if not embedding_result.get("success", False):
        return embedding_result

    # Return combined result
    return {
        "success": True,
        "metadata_result": metadata_result,
        "ocr_result": ocr_result if ocr_result.get("success", False) else None,
        "embedding_result": embedding_result,
        "bucket": metadata_result.get("bucket", ""),
        "key": metadata_result.get("key", ""),
        "embedding_dimensions": embedding_result.get("dimensions", 0),
        "model_id": model_id,
        "has_ocr_content": ocr_result.get("success", False),
    }


def embed_asset_with_translation(
    metadata_result: dict,
    translation_result: dict,
    model_id: str = "amazon.titan-embed-text-v1",
) -> dict:
    """
    Embed asset metadata with translated text.

    Args:
        metadata_result: Metadata result from object_metadata.py
        translation_result: Translation result from stored_text_translate.py
        model_id: Bedrock model ID (default: 'amazon.titan-embed-text-v1')

    Returns:
        Dictionary with embedding results
    """
    if not metadata_result.get("success", False):
        return {
            "success": False,
            "error": "Metadata result was not successful",
            "metadata_result": metadata_result,
        }

    text_content = ""
    if translation_result.get("success", False):
        text_content = translation_result.get("translated_text", "")

    # Embed metadata and translated text
    embedding_result = embed_object_metadata_and_text(
        metadata=metadata_result, text=text_content, model_id=model_id
    )

    if not embedding_result.get("success", False):
        return embedding_result

    # Return combined result
    return {
        "success": True,
        "metadata_result": metadata_result,
        "translation_result": translation_result
        if translation_result.get("success", False)
        else None,
        "embedding_result": embedding_result,
        "bucket": metadata_result.get("bucket", ""),
        "key": metadata_result.get("key", ""),
        "embedding_dimensions": embedding_result.get("dimensions", 0),
        "model_id": model_id,
        "has_translation_content": translation_result.get("success", False),
        "source_language": translation_result.get("source_language", "")
        if translation_result.get("success", False)
        else "",
        "target_language": translation_result.get("target_language", "")
        if translation_result.get("success", False)
        else "",
    }
