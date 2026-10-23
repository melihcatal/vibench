import boto3
import json
import os

def create_embedding(payload, config=None):
    config = config or {}
    region = config.get("region", "us-east-1")
    client = boto3.client("bedrock-runtime", region_name=region)

    text_to_embed = payload.get("text", "")
    embedding_model_id = config.get("embedding_model_id", "amazon.titan-embed-text-v1")

    # The request body for Titan Embed Text model
    body = json.dumps({"inputText": text_to_embed})

    response = client.invoke_model(
        body=body,
        modelId=embedding_model_id,
        accept="application/json",
        contentType="application/json",
    )

    response_body = json.loads(response.get("body").read())
    embedding = response_body.get("embedding")

    return {"embedding": embedding}
