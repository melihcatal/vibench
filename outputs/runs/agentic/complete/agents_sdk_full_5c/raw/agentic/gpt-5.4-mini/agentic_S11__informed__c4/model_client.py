from __future__ import annotations

import os
from typing import Any, Dict, Optional

import boto3
from botocore.config import Config

from model_models import PlatformRequest, PlatformResponse, StreamChunk, normalize_text


DEFAULT_MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"


def load_platform_config() -> Dict[str, Any]:
    return {
        "aws_region": os.getenv("AWS_REGION", "us-east-1"),
        "bedrock_model_id": os.getenv("BEDROCK_MODEL_ID", DEFAULT_MODEL_ID),
        "output_locale": os.getenv("OUTPUT_LOCALE", "es"),
        "tts_voice_id": os.getenv("TTS_VOICE_ID", "Joanna"),
    }


def bedrock_runtime_client(region_name: Optional[str] = None):
    cfg = Config(retries={"max_attempts": 3, "mode": "standard"})
    return boto3.client("bedrock-runtime", region_name=region_name or load_platform_config()["aws_region"], config=cfg)


def bedrock_client(region_name: Optional[str] = None):
    cfg = Config(retries={"max_attempts": 3, "mode": "standard"})
    return boto3.client("bedrock", region_name=region_name or load_platform_config()["aws_region"], config=cfg)


def build_converse_input(request: PlatformRequest) -> Dict[str, Any]:
    return {
        "modelId": request.model,
        "messages": [{"role": "user", "content": [{"text": request.prompt}]}],
        "inferenceConfig": {
            "maxTokens": request.max_tokens,
            "temperature": request.temperature,
        },
    }


def extract_bedrock_text(response: Dict[str, Any]) -> str:
    outputs = []
    for message in response.get("output", {}).get("message", {}).get("content", []):
        if isinstance(message, dict) and "text" in message:
            outputs.append(message["text"])
    if outputs:
        return normalize_text(outputs)
    return normalize_text([response.get("output", {}).get("text", "")])


def collect_platform_response(response: Dict[str, Any]) -> PlatformResponse:
    text = extract_bedrock_text(response)
    usage = response.get("usage", {}) or {}
    model_id = response.get("modelId")
    resource_id = response.get("ResponseMetadata", {}).get("RequestId")
    return PlatformResponse(text=text, usage=usage, resource_id=resource_id, model_id=model_id, raw=response)


def stream_to_chunks(stream_response: Any):
    for event in stream_response.get("stream", []):
        if "contentBlockDelta" in event:
            delta = event["contentBlockDelta"].get("delta", {})
            text = delta.get("text", "")
            yield StreamChunk(text=text, raw=event)
