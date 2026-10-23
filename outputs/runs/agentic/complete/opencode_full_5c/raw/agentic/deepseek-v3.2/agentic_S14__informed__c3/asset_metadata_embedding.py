import boto3
import os
import json
from botocore.exceptions import ClientError


def embed_asset_metadata(metadata_text, model_id="amazon.titan-embed-text-v2:0"):
    """
    Embed object metadata and extracted text for search using Amazon Titan Embeddings.

    Args:
        metadata_text: Text containing metadata and/or extracted content
        model_id: Bedrock embedding model ID (default: Titan Embed Text v2)

    Returns:
        dict: Embedding results including vector and model information
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise EnvironmentError(
            "AWS credentials not found. Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables."
        )

    bedrock_runtime = boto3.client(
        "bedrock-runtime",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )

    try:
        if model_id.startswith("amazon.titan-embed"):
            body = json.dumps({"inputText": metadata_text})
        else:
            raise ValueError(f"Unsupported embedding model: {model_id}")

        response = bedrock_runtime.invoke_model(modelId=model_id, body=body)

        response_body = json.loads(response["body"].read())

        if model_id.startswith("amazon.titan-embed"):
            embedding = response_body.get("embedding", [])
            dimensions = len(embedding)
        else:
            embedding = []
            dimensions = 0

        return {
            "text": metadata_text,
            "embedding": embedding,
            "dimensions": dimensions,
            "model_id": model_id,
            "provider": "Amazon Titan Embeddings via Bedrock",
        }
    except ClientError as e:
        raise Exception(
            f"Failed to generate embeddings using Amazon Titan Embeddings: {e}"
        )
