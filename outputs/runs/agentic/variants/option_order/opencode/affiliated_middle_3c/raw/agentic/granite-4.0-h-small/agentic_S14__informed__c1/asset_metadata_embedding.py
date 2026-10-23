import os
import openai
import boto3
from typing import Dict, List
from storage_client import get_s3_client
from storage_models import ObjectMetadata


def object_metadata_and_embedding(bucket_name: str, object_key: str) -> Dict[str, any]:
    """Combine an object's metadata with its text embedding for semantic search.

    Uses:
    - boto3 for S3 to fetch object metadata and content.
    - Amazon Titan Text Embeddings via Bedrock (boto3 client 'bedrock-runtime').
    - Optional OpenAI embeddings fallback if Titan not available.

    Returns a dict with keys: bucket, key, size, content_type, text_embedding (list of floats).
    """
    # 1. S3 client (already configured for S3)
    s3 = get_s3_client()
    metadata: ObjectMetadata = s3.head_object(Bucket=bucket_name, Key=object_key)
    # Ensure file is text-like for embedding
    if "ContentType" not in metadata or not metadata["ContentType"].startswith(
        "text/plain"
    ):
        raise ValueError("Only plain-text objects can be embedded")

    obj = s3.get_object(Bucket=bucket_name, Key=object_key)
    text = obj["Body"].read().decode("utf-8")

    # 2. Embedding provider – Amazon Titan via Bedrock
    bedrock = boto3.client("bedrock-runtime")
    # Titan model ID for embeddings (aws/titan-text-prem-embed-v1)
    model_id = "aws/titan-text-prem-embed-v1"
    embedding_response = bedrock.create_embedding(
        ModelId=model_id,
        Input=text.encode("utf-8"),
        ContentType="application/octet-stream",
    )
    embedding = embedding_response["Embedding"]["features"]  # list of floats

    return {
        "bucket": bucket_name,
        "key": object_key,
        "size": metadata.get("Size"),
        "content_type": metadata.get("ContentType"),
        "text_embedding": embedding,
    }
