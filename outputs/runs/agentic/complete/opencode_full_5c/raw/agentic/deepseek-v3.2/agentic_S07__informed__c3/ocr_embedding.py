import os
from typing import List, Optional
import boto3
import json
from botocore.exceptions import ClientError


def ocr_embedding(text: str, region: Optional[str] = None) -> List[float]:
    """Embed extracted document sections for semantic retrieval using Amazon Titan Embeddings.

    Args:
        text: Text to embed
        region: AWS region (defaults to AWS_DEFAULT_REGION env var)

    Returns:
        Embedding vector as list of floats
    """
    # Initialize Bedrock Runtime client
    region_name = region or os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    client = boto3.client(
        "bedrock-runtime",
        region_name=region_name,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    # Prepare request for Titan Embeddings model
    model_id = "amazon.titan-embed-text-v2:0"

    body = json.dumps(
        {
            "inputText": text,
            "dimensions": 1024,  # Titan v2 supports configurable dimensions
            "normalize": True,
        }
    )

    try:
        # Call Bedrock Runtime API
        response = client.invoke_model(
            modelId=model_id,
            body=body,
            contentType="application/json",
            accept="application/json",
        )

        # Parse response
        response_body = json.loads(response["body"].read())
        embedding = response_body.get("embedding", [])

        return embedding

    except ClientError as e:
        raise Exception(f"Bedrock Runtime API error: {e}")
