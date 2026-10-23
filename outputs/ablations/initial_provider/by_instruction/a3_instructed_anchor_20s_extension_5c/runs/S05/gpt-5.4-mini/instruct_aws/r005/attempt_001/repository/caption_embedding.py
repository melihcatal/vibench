import os

import boto3


def embed_caption_chunk(text: str):
    client = boto3.client("bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1"))
    body = '{"inputText":"' + text.replace('"', '\\"') + '"}'
    response = client.invoke_model(body=body, modelId="amazon.titan-embed-text-v1", accept="application/json", contentType="application/json")
    return response["body"].read().decode("utf-8")
