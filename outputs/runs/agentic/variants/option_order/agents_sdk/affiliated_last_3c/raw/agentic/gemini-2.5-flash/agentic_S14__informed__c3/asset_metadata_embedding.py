import os
import boto3
import json
from typing import List

def get_titan_text_embeddings(text_list: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of texts using Amazon Titan Embeddings via Bedrock Runtime.

    Args:
        text_list (List[str]): A list of texts to embed.

    Returns:
        List[List[float]]: A list of embedding vectors, one for each input text.
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set in environment variables.")

    bedrock_runtime_client = boto3.client(
        "bedrock-runtime",
        region_name=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    model_id = "amazon.titan-embed-text-v1"
    embeddings = []

    for text in text_list:
        body = json.dumps({
            "inputText": text
        })

        response = bedrock_runtime_client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=body
        )

        response_body = json.loads(response['body'].read())
        embeddings.append(response_body['embedding'])

    return embeddings
