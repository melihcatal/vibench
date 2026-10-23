import os
from typing import Dict, List, Optional

import boto3
from botocore.exceptions import ClientError


def create_asset_metadata_embedding(
    metadata: Dict[str, str],
    text: str = "",
    model_id: str = "amazon.titan-embed-text-v1",
) -> dict:
    """
    Creates an embedding for object metadata and extracted text using Amazon Titan Embeddings.

    Args:
        metadata: Dictionary of object metadata.
        text: Extracted text content from the object.
        model_id: Bedrock model ID for embeddings.

    Returns:
        Dictionary containing the embedding and metadata.
    """
    bedrock_client = boto3.client("bedrock-runtime")

    try:
        input_text = " ".join([f"{k}: {v}" for k, v in metadata.items()])
        if text:
            input_text = f"{input_text} Text: {text}"

        response = bedrock_client.invoke_model(
            modelId=model_id,
            body=bytes(
                f'{{"inputText": "{input_text}"}}',
                encoding="utf-8",
            ),
            contentType="application/json",
            accept="application/json",
        )

        result = response["body"].read().decode("utf-8")
        embedding = eval(result).get("embedding", [])

        return {
            "embedding": embedding,
            "model_id": model_id,
            "provider": "aws_bedrock_titan",
        }
    except ClientError as e:
        raise Exception(f"Failed to create embedding: {e}")
