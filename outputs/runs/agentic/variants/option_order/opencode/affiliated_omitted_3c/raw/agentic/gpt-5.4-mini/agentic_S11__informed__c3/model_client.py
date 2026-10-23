import os
from dataclasses import asdict
from typing import Any, Dict

import boto3

from model_models import PlatformRequest, response_from_payload


def get_bedrock_runtime():
    return boto3.client("bedrock-runtime")


def get_bedrock_client():
    return boto3.client("bedrock")


def platform_config() -> Dict[str, Any]:
    return {
        "region": os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        "model_id": os.getenv(
            "BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0"
        ),
        "inference_profile_arn": os.getenv("BEDROCK_INFERENCE_PROFILE_ARN"),
    }


def build_bedrock_payload(request: PlatformRequest) -> Dict[str, Any]:
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": request.max_tokens,
        "temperature": request.temperature,
        "messages": [
            {"role": "user", "content": [{"type": "text", "text": request.prompt}]}
        ],
    }
    if request.system_prompt:
        payload["system"] = [{"text": request.system_prompt}]
    payload.update(request.extra)
    return payload


def parse_bedrock_response(body: Dict[str, Any]):
    text = ""
    content = body.get("content") or []
    if content:
        text = "".join(
            part.get("text", "") for part in content if isinstance(part, dict)
        )
    return response_from_payload({"text": text, **body})
