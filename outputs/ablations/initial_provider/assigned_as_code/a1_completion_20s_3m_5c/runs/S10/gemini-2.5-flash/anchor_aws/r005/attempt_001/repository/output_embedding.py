import boto3
import os
import json


def embed_output(payload, config=None):
    config = config or {}
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    client = boto3.client("bedrock-runtime", region_name=aws_region)

    text_to_embed = payload["text"]
    embedding_model_id = os.environ.get("BEDROCK_EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v1")

    # Bedrock embedding models typically expect a specific payload structure
    request_body = json.dumps({"inputText": text_to_embed})

    response = client.invoke_model(
        body=request_body,
        modelId=embedding_model_id,
        accept="application/json",
        contentType="application/json"
    )

    response_body = json.loads(response.get("body").read())
    embedding = response_body.get("embedding")

    return {"embedding": embedding, "model_id": embedding_model_id}
