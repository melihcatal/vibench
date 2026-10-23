import os
from dataclasses import dataclass
from typing import Optional

import boto3


@dataclass
class ModelConfig:
    region: str
    model_id: str
    temperature: float = 0.2
    max_tokens: int = 1024
    top_p: float = 0.9


def get_config(default_model_id: str) -> ModelConfig:
    return ModelConfig(
        region=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")),
        model_id=os.getenv("BEDROCK_MODEL_ID", default_model_id),
        temperature=float(os.getenv("MODEL_TEMPERATURE", "0.2")),
        max_tokens=int(os.getenv("MODEL_MAX_TOKENS", "1024")),
        top_p=float(os.getenv("MODEL_TOP_P", "0.9")),
    )


def bedrock_runtime_client(region: Optional[str] = None):
    return boto3.client("bedrock-runtime", region_name=region or os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")))


def family_from_model_id(model_id: str) -> str:
    lowered = model_id.lower()
    if "claude" in lowered:
        return "anthropic.claude"
    if "llama" in lowered:
        return "meta.llama"
    if "mistral" in lowered:
        return "mistral"
    if "nova" in lowered:
        return "amazon.nova"
    return "generic"
