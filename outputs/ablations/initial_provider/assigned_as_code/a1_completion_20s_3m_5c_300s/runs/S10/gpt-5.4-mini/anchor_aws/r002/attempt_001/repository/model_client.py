import os
from dataclasses import dataclass

import boto3


DEFAULT_MODEL_ID = "amazon.nova-pro-v1:0"


@dataclass
class ModelConfig:
    region: str | None = None
    model_id: str = DEFAULT_MODEL_ID
    temperature: float = 0.0
    max_tokens: int = 1024
    stream: bool = False


def load_config(config=None):
    data = dict(config or {})
    return ModelConfig(
        region=data.get("region") or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        model_id=data.get("model_id") or os.getenv("BEDROCK_MODEL_ID") or DEFAULT_MODEL_ID,
        temperature=float(data.get("temperature", 0.0)),
        max_tokens=int(data.get("max_tokens", 1024)),
        stream=bool(data.get("stream", False)),
    )


def client(config=None):
    cfg = load_config(config)
    return boto3.client("bedrock-runtime", region_name=cfg.region), cfg


def converse_messages(prompt):
    return [{"role": "user", "content": [{"text": prompt}]}]


def extract_converse_text(response):
    return "".join(
        block["text"] for block in response["output"]["message"]["content"] if "text" in block
    )
