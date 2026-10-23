import os
from typing import Dict, List, Optional

import boto3
from botocore.exceptions import ClientError


def asset_metadata_embedding(
    metadata: Dict[str, str],
    text: Optional[str] = None,
    model_id: str = "amazon.titan-embed-text-v1",
) -> List[float]:
    """
    Embeds object metadata and extracted text for search using Amazon Bedrock.

    Args:
        metadata: Dictionary of object metadata.
        text: Optional extracted text content.
        model_id: Bedrock embedding model ID (default: amazon.titan-embed-text-v1).

    Returns:
        List[float]: Embedding vector for the input.
    """
    bedrock = boto3.client(
        "bedrock-runtime",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    input_text = "\n".join([f"{k}: {v}" for k, v in metadata.items()])
    if text:
        input_text += f"\nContent: {text}"

    try:
        response = bedrock.invoke_model(
            modelId=model_id,
            body=bytes(f'{{"inputText":"{input_text}"}}', "utf-8"),
            contentType="application/json",
            accept="application/json",
        )
        result = response["body"].read().decode("utf-8")
        return eval(result).get("embedding", [])
    except ClientError as e:
        raise Exception(f"Failed to generate embedding using Amazon Bedrock: {e}")
