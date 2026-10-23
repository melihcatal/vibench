import os
import json
from typing import Dict, List, Optional
import boto3
import numpy as np
from storage_client import get_storage_client
from storage_models import ObjectMetadataResponse

def embed_asset_metadata_and_text(
    object_key: str,
    extracted_text: Optional[str] = None,
    output_object_key: Optional[str] = None
) -> List[float]:
    """
    Embeds object metadata and extracted text for search using AWS Bedrock.
    Returns the embedding vector.
    """
    s3_client = get_storage_client()
    bedrock_client = boto3.client(
        "bedrock-runtime",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1")
    )

    bucket_name = os.getenv("AWS_S3_BUCKET_NAME", "default-bucket")
    output_key = output_object_key or f"embedding-output/{object_key}.json"

    # Fetch metadata
    from object_metadata import get_object_metadata
    metadata_response: ObjectMetadataResponse = get_object_metadata(
        ObjectMetadataRequest(object_key=object_key)
    )

    # Prepare input for embedding
    input_text = f"Metadata: {json.dumps(metadata_response.metadata)}"
    if extracted_text:
        input_text += f"\nExtracted Text: {extracted_text}"

    body = {
        "inputText": input_text
    }

    bedrock_response = bedrock_client.invoke_model(
        modelId="amazon.titan-embed-text-v1",
        body=bytes(json.dumps(body).encode("utf-8"))
    )

    response_body = json.loads(bedrock_response["body"].read().decode("utf-8"))
    embedding = response_body["embedding"]

    # Store embedding
    s3_client.put_object(
        Bucket=bucket_name,
        Key=output_key,
        Body=json.dumps({"embedding": embedding}).encode("utf-8")
    )

    return embedding