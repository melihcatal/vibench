import json
from typing import List

from safety_client import bedrock_runtime_client, load_model_id


DEFAULT_MODEL_ID = "amazon.titan-embed-text-v1"


def moderation_reason_embedding(reason: str) -> List[float]:
    client = bedrock_runtime_client()
    model_id = load_model_id(DEFAULT_MODEL_ID)
    response = client.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=json.dumps({"inputText": reason}).encode("utf-8"),
    )
    raw = json.loads(response["body"].read().decode("utf-8"))
    return list(raw.get("embedding", []))
