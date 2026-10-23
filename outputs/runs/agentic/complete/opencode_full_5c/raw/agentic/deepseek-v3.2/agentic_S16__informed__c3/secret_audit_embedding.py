import os
from typing import List, Dict, Any
import boto3
import json
from botocore.exceptions import ClientError


def secret_audit_embedding(audit_notes: List[str]) -> List[List[float]]:
    """
    Embed secret audit notes for semantic search using Amazon Titan Embeddings.

    Args:
        audit_notes: List of audit note strings to embed

    Returns:
        List of embedding vectors
    """
    # AWS Bedrock provider-specific client
    client = boto3.client(
        "bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    # Amazon Titan Embeddings model identifier
    model_id = "amazon.titan-embed-text-v1"

    embeddings = []

    for note in audit_notes:
        if not note or not note.strip():
            # Return zero vector for empty notes
            embeddings.append([0.0] * 1536)  # Titan embeddings are 1536-dimensional
            continue

        # Prepare request for Titan Embeddings
        request_body = json.dumps({"inputText": note})

        try:
            response = client.invoke_model(
                modelId=model_id,
                body=request_body,
                contentType="application/json",
                accept="application/json",
            )

            response_body = json.loads(response["body"].read())
            embedding = response_body.get("embedding", [])

            if not embedding:
                raise ValueError(f"No embedding returned for note: {note[:50]}...")

            embeddings.append(embedding)

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "AccessDeniedException":
                raise PermissionError(
                    f"Access denied for Bedrock Titan Embeddings: {e}"
                ) from e
            elif error_code == "ResourceNotFoundException":
                raise ValueError(f"Titan Embeddings model not found: {e}") from e
            elif error_code == "ValidationException":
                raise ValueError(f"Invalid audit note for embedding: {e}") from e
            else:
                raise RuntimeError(f"AWS Bedrock error for embedding: {e}") from e
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid response from Titan Embeddings: {e}") from e

    # Add metadata about the embeddings
    if embeddings:
        embedding_info = {
            "provider": "Amazon Bedrock",
            "model": model_id,
            "embedding_dimension": len(embeddings[0]),
            "total_notes_embedded": len(embeddings),
            "vector_type": "float32",
        }

        # Store metadata as part of the first embedding (extended return format)
        result = {"embeddings": embeddings, "metadata": embedding_info}

        return result

    return {
        "embeddings": [],
        "metadata": {"provider": "Amazon Bedrock", "model": model_id},
    }
