import json
import os

import boto3


DEFAULT_REGION = os.getenv("AWS_REGION", "us-east-1")
DEFAULT_MODEL_ID = os.getenv("BEDROCK_EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v2:0")


def get_bedrock_client(config=None):
    config = config or {}
    return boto3.client("bedrock-runtime", region_name=config.get("region", DEFAULT_REGION))


def get_model_id(config=None):
    config = config or {}
    return config.get("model_id", DEFAULT_MODEL_ID)


def invoke_embedding(client, model_id, text):
    response = client.invoke_model(
        modelId=model_id,
        body=json.dumps({"inputText": text}),
        contentType="application/json",
        accept="application/json",
    )
    stream = response["body"]
    try:
        return json.loads(stream.read())
    finally:
        stream.close()
