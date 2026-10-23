import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional

import boto3


@dataclass(frozen=True)
class ModelConfig:
    region: str
    model_id: str


def load_model_config(default_model_id: str) -> ModelConfig:
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    model_id = os.getenv("AWS_BEDROCK_MODEL_ID") or default_model_id
    return ModelConfig(region=region, model_id=model_id)


def bedrock_runtime(region: Optional[str] = None):
    session = boto3.session.Session(region_name=region)
    return session.client("bedrock-runtime")


def invoke_json_model(client, model_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    response = client.invoke_model(modelId=model_id, body=body, accept="application/json", contentType="application/json")
    raw = response["body"].read()
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8")
    return json.loads(raw)


def stream_model(client, model_id: str, payload: Dict[str, Any]) -> Iterable[str]:
    body = json.dumps(payload).encode("utf-8")
    response = client.invoke_model_with_response_stream(modelId=model_id, body=body, accept="application/json", contentType="application/json")
    for event in response["body"]:
        if "chunk" in event:
            chunk = event["chunk"]["bytes"].decode("utf-8")
            if chunk:
                yield chunk
