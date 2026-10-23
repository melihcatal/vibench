import json
import os

import boto3


def get_region(config=None):
    config = config or {}
    return config.get("region") or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1"


def get_bedrock_client(config=None):
    return boto3.client("bedrock-runtime", region_name=get_region(config))


def get_model_id(config=None):
    config = config or {}
    return config.get("model_id") or "amazon.titan-embed-text-v2:0"


def invoke_bedrock_json(client, model_id, payload):
    response = client.invoke_model(modelId=model_id, body=json.dumps(payload), contentType="application/json", accept="application/json")
    body = response["body"]
    try:
        return json.loads(body.read())
    finally:
        body.close()
