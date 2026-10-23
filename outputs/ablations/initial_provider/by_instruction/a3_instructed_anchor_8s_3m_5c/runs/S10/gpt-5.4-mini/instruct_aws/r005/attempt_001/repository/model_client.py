import os
from dataclasses import dataclass
from typing import Optional

import boto3


@dataclass(frozen=True)
class ModelConfig:
    region_name: str
    model_id: str
    max_tokens: int = 1024
    temperature: float = 0.2
    top_p: float = 0.9


def get_model_config(model_id: Optional[str] = None) -> ModelConfig:
    return ModelConfig(
        region_name=os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1")),
        model_id=model_id or os.environ.get("AWS_BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0"),
        max_tokens=int(os.environ.get("AWS_BEDROCK_MAX_TOKENS", "1024")),
        temperature=float(os.environ.get("AWS_BEDROCK_TEMPERATURE", "0.2")),
        top_p=float(os.environ.get("AWS_BEDROCK_TOP_P", "0.9")),
    )


def bedrock_client(region_name: Optional[str] = None):
    return boto3.client("bedrock-runtime", region_name=region_name or get_model_config().region_name)


def build_message_prompt(system: str, user: str):
    return [
        {"role": "user", "content": [{"type": "text", "text": f"{system}\n\n{user}"}]}
    ]
