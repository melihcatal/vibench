from speech_client import load_config

import boto3


def script_embedding(payload, config=None):
    cfg = load_config(config)
    client = boto3.client("bedrock-runtime", region_name=cfg["region"])
    body = {"inputText": payload["text"]}
    response = client.invoke_model(modelId=payload.get("model_id", "amazon.titan-embed-text-v1"), body=str(body).encode("utf-8"), accept="application/json", contentType="application/json")
    return {"embedding_body": response["body"].read(), "model_id": payload.get("model_id", "amazon.titan-embed-text-v1")}
