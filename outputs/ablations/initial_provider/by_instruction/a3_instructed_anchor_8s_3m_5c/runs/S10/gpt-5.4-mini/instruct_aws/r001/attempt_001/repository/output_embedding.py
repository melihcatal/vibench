import json

from model_client import bedrock_runtime, load_model_config


def output_embedding(text: str) -> list[float]:
    config = load_model_config("amazon.titan-embed-text-v1")
    client = bedrock_runtime(config.region)
    body = json.dumps({"inputText": text}).encode("utf-8")
    response = client.invoke_model(modelId=config.model_id, body=body, accept="application/json", contentType="application/json")
    raw = response["body"].read()
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8")
    data = json.loads(raw)
    return data.get("embedding", [])
