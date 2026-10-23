import boto3
import os
import json
from typing import List

def script_embedding(text: str) -> List[float]:
    """
    Embeds narration scripts using Amazon Titan Embeddings via Bedrock Runtime.

    Args:
        text: The script text to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    bedrock_runtime_client = boto3.client(
        'bedrock-runtime',
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )

    model_id = "amazon.titan-embed-text-v1"
    accept = "application/json"
    content_type = "application/json"

    body = json.dumps({"inputText": text})

    response = bedrock_runtime_client.invoke_model(
        body=body,
        modelId=model_id,
        accept=accept,
        contentType=content_type
    )

    response_body = json.loads(response.get('body').read())
    embedding = response_body.get('embedding')
    return embedding
