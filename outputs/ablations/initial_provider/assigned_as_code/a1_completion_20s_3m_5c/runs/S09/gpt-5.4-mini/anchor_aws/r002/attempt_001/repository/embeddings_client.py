import json
import os

import boto3


def get_config(config=None):
    base = dict(config or {})
    base.setdefault("region", os.getenv("AWS_REGION", "us-east-1"))
    base.setdefault("model_id", os.getenv("BEDROCK_EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v2:0"))
    return base


def get_client(config=None):
    config = get_config(config)
    return boto3.client("bedrock-runtime", region_name=config["region"])


def invoke_embedding(client, model_id, body):
    response = client.invoke_model(modelId=model_id, body=json.dumps(body), contentType="application/json", accept="application/json")
    stream = response["body"]
    try:
        return json.loads(stream.read())
    finally:
        stream.close()
