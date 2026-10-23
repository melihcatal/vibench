import json
import os

import boto3


def load_config(config=None):
    config = config or {}
    return {
        "region": config.get("region") or os.environ.get("AWS_REGION", "us-east-1"),
        "model_id": config.get("model_id") or os.environ.get("BEDROCK_EMBEDDINGS_MODEL_ID", "amazon.titan-embed-text-v2:0"),
    }


def create_client(config=None):
    cfg = load_config(config)
    return boto3.client("bedrock-runtime", region_name=cfg["region"]), cfg


def invoke_embedding(client, model_id, text):
    response = client.invoke_model(modelId=model_id, body=json.dumps({"inputText": text}), contentType="application/json", accept="application/json")
    stream = response["body"]
    try:
        return json.loads(stream.read())["embedding"]
    finally:
        stream.close()


def invoke_batch_embeddings(client, model_id, texts):
    return [invoke_embedding(client, model_id, text) for text in texts]
