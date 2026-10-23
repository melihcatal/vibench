import boto3
import os
import json

def embed_batch(texts: list[str]) -> list[list[float]]:
    """
    Generates embedding vectors for a batch of text strings using AWS Bedrock.
    """
    bedrock = boto3.client(
        service_name="bedrock-runtime",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    model_id = "amazon.titan-embed-text-v1"

    embeddings = []
    for text in texts:
        response = bedrock.invoke_model(
            body=f'{{"inputText": "{text}"}}',
            modelId=model_id,
            accept="application/json",
            contentType="application/json",
        )
        response_body = json.loads(response.get("body").read())
        embeddings.append(response_body["embedding"])
    return embeddings
