import boto3
import json
import os
from typing import List, Dict, Any
from botocore.exceptions import ClientError
from storage_client import get_s3_client
from storage_models import EmbeddingResult


def embed_text_with_titan(text, model_id="amazon.titan-embed-text-v2:0"):
    """
    Embed text using Amazon Titan Embeddings via Bedrock.

    Args:
        text: Text to embed
        model_id: Titan embedding model ID

    Returns:
        dict: Embedding results or error
    """
    bedrock_runtime = boto3.client("bedrock-runtime")

    try:
        # Prepare request for Titan embeddings
        body = json.dumps({"inputText": text})

        # Invoke model
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=body,
        )

        # Parse response
        response_body = json.loads(response["body"].read())
        embedding = response_body.get("embedding", [])

        return {
            "success": True,
            "text": text,
            "embedding": embedding,
            "dimensions": len(embedding),
            "model_id": model_id,
            "provider": "Amazon Bedrock (Titan Embeddings)",
        }

    except ClientError as e:
        return {"success": False, "error": str(e), "provider": "Amazon Bedrock"}
    except Exception as e:
        return {"success": False, "error": str(e), "provider": "Amazon Bedrock"}


def embed_object_metadata_and_text(bucket_name, object_key, include_content=True):
    """
    Embed object metadata and extracted text for search.

    Args:
        bucket_name: S3 bucket name
        object_key: S3 object key
        include_content: Whether to include extracted text content

    Returns:
        dict: Combined metadata and embedding results
    """
    # Get object metadata
    from object_metadata import get_object_metadata

    metadata_result = get_object_metadata(bucket_name, object_key)

    if not metadata_result.get("success"):
        return {
            "success": False,
            "error": f"Metadata retrieval failed: {metadata_result.get('error')}",
            "provider": "Amazon Bedrock + S3",
        }

    # Prepare metadata text for embedding
    metadata_text = f"""
    Object Key: {object_key}
    Bucket: {bucket_name}
    Content Type: {metadata_result.get("content_type", "unknown")}
    Size: {metadata_result.get("content_length", 0)} bytes
    Last Modified: {metadata_result.get("last_modified")}
    Storage Class: {metadata_result.get("storage_class", "STANDARD")}
    """

    # Add user metadata if present
    if "user_metadata" in metadata_result and metadata_result["user_metadata"]:
        metadata_text += "\nUser Metadata:\n"
        for key, value in metadata_result["user_metadata"].items():
            metadata_text += f"{key}: {value}\n"

    content_text = ""
    if include_content:
        # Try to extract text content
        file_ext = os.path.splitext(object_key)[1].lower()

        if file_ext in [".txt", ".md", ".csv", ".json", ".xml", ".html", ".htm"]:
            # Read text files directly
            try:
                s3_client = get_s3_client()
                response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
                content_text = response["Body"].read().decode("utf-8", errors="ignore")
                content_text = content_text[:2000]  # Limit length
            except:
                content_text = "[Text content not accessible]"

        elif file_ext in [".pdf", ".jpg", ".jpeg", ".png", ".tiff", ".tif"]:
            # Use OCR for documents/images
            from stored_document_ocr import run_ocr_on_stored_document

            ocr_result = run_ocr_on_stored_document(bucket_name, object_key)
            if ocr_result.get("success"):
                content_text = ocr_result.get("text", "")[:2000]  # Limit length
            else:
                content_text = "[OCR extraction failed]"
        else:
            content_text = "[Binary file - content not extracted]"

    # Combine metadata and content for embedding
    combined_text = f"""
    OBJECT METADATA:
    {metadata_text}
    
    EXTRACTED CONTENT:
    {content_text if content_text else "[No content extracted]"}
    """

    # Generate embedding
    embedding_result = embed_text_with_titan(combined_text)

    if embedding_result.get("success"):
        return {
            "success": True,
            "bucket": bucket_name,
            "key": object_key,
            "metadata": {
                "content_type": metadata_result.get("content_type"),
                "size": metadata_result.get("content_length"),
                "last_modified": metadata_result.get("last_modified"),
                "storage_class": metadata_result.get("storage_class"),
            },
            "content_extracted": bool(
                content_text
                and content_text
                not in [
                    "[Text content not accessible]",
                    "[OCR extraction failed]",
                    "[Binary file - content not extracted]",
                    "[No content extracted]",
                ]
            ),
            "content_sample": content_text[:500] if content_text else "",
            "embedding": embedding_result.get("embedding"),
            "embedding_dimensions": embedding_result.get("dimensions"),
            "model_id": embedding_result.get("model_id"),
            "provider": "Amazon Bedrock (Titan Embeddings) + S3",
        }
    else:
        return {
            "success": False,
            "error": f"Embedding failed: {embedding_result.get('error')}",
            "metadata_retrieved": True,
            "metadata": {
                "content_type": metadata_result.get("content_type"),
                "size": metadata_result.get("content_length"),
            },
            "provider": "Amazon Bedrock + S3",
        }


def batch_embed_objects(bucket_name, prefix="", max_objects=10):
    """
    Batch embed multiple objects under a prefix.

    Args:
        bucket_name: S3 bucket name
        prefix: Object prefix
        max_objects: Maximum number of objects to process

    Returns:
        dict: Batch embedding results
    """
    # List objects
    from list_prefix import list_objects_with_prefix

    list_result = list_objects_with_prefix(bucket_name, prefix, max_keys=max_objects)

    if not list_result.get("success"):
        return {
            "success": False,
            "error": f"List objects failed: {list_result.get('error')}",
            "provider": "Amazon Bedrock + S3",
        }

    objects = list_result.get("objects", [])
    if not objects:
        return {
            "success": True,
            "message": "No objects found",
            "objects_processed": 0,
            "embeddings": [],
            "provider": "Amazon Bedrock + S3",
        }

    # Process each object
    embeddings = []
    errors = []

    for obj in objects[:max_objects]:
        obj_key = obj["key"]
        try:
            embed_result = embed_object_metadata_and_text(bucket_name, obj_key)
            if embed_result.get("success"):
                embeddings.append(
                    {
                        "key": obj_key,
                        "size": obj["size"],
                        "embedding_dimensions": embed_result.get(
                            "embedding_dimensions"
                        ),
                        "content_extracted": embed_result.get("content_extracted"),
                        "model_id": embed_result.get("model_id"),
                    }
                )
            else:
                errors.append({"key": obj_key, "error": embed_result.get("error")})
        except Exception as e:
            errors.append({"key": obj_key, "error": str(e)})

    return {
        "success": True,
        "objects_processed": len(embeddings),
        "errors_count": len(errors),
        "embeddings": embeddings,
        "errors": errors if errors else None,
        "provider": "Amazon Bedrock (Titan Embeddings) + S3",
    }
