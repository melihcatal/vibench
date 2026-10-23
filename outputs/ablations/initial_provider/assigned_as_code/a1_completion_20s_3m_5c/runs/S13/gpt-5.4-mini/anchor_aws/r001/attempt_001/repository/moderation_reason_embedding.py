import json

from safety_client import get_bedrock_runtime_client
from safety_models import normalize_text


def moderation_reason_embedding(payload, config=None):
    config = config or {}
    client = get_bedrock_runtime_client(config)
    text = normalize_text(payload.get("text"))
    body = json.dumps({"inputText": text})
    response = client.invoke_model(
        modelId=config.get("model_id", "amazon.titan-embed-text-v1"),
        body=body.encode("utf-8"),
        contentType="application/json",
        accept="application/json",
    )
    return {"embedding": response["body"].read().decode("utf-8")}
