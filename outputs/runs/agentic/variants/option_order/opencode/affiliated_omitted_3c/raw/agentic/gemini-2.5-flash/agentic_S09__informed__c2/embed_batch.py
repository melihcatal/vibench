import os
import boto3
from typing import List, Dict, Any


def embed_batch(texts: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a batch of texts using Amazon Titan Embeddings via Bedrock Runtime.
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")  # Default region

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables not set."
        )

    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime",
        region_name=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    # The model_id "amazon.titan-embed-text-v1" is a concrete identifier for Amazon Titan's embedding model.
    # It's explicitly mentioned in AWS Bedrock documentation.
    body = {"inputText": texts}
    response = bedrock_runtime.invoke_model(
        modelId="amazon.titan-embed-text-v1",
        contentType="application/json",
        accept="application/json",
        body=str(body),  # boto3 requires body to be a string
    )

    response_body = json.loads(response.get("body").read())
    embeddings = [item["embedding"] for item in response_body.get("embeddings", [])]

    return embeddings


import json
