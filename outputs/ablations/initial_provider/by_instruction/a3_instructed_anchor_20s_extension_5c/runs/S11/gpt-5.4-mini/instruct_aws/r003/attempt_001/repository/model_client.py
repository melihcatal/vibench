import os
from typing import Any, Dict, Optional

import boto3
from botocore.config import Config

from model_models import PlatformRequest


def load_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def load_bedrock_runtime_client():
    return boto3.client(
        "bedrock-runtime",
        region_name=load_region(),
        config=Config(retries={"max_attempts": 3, "mode": "standard"}),
    )


def load_bedrock_client():
    return boto3.client(
        "bedrock",
        region_name=load_region(),
        config=Config(retries={"max_attempts": 3, "mode": "standard"}),
    )


def default_model_id() -> str:
    return os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")


def build_invoke_payload(request: PlatformRequest) -> Dict[str, Any]:
    return {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": request.max_tokens,
        "temperature": request.temperature,
        "messages": [{"role": "user", "content": request.prompt}],
    }


def model_id_for_request(request: Optional[PlatformRequest] = None) -> str:
    if request and request.model_id:
        return request.model_id
    return default_model_id()
