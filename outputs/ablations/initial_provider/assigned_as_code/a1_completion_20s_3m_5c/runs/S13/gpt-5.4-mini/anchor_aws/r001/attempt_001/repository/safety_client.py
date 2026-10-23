import os
from typing import Any, Dict

import boto3

from safety_models import normalize_text


def get_region(config: Dict[str, Any] = None) -> str:
    config = config or {}
    return config.get("region") or os.getenv("AWS_REGION") or "us-east-1"


def get_comprehend_client(config: Dict[str, Any] = None):
    return boto3.client("comprehend", region_name=get_region(config))


def get_translate_client(config: Dict[str, Any] = None):
    return boto3.client("translate", region_name=get_region(config))


def get_polly_client(config: Dict[str, Any] = None):
    return boto3.client("polly", region_name=get_region(config))


def get_bedrock_runtime_client(config: Dict[str, Any] = None):
    return boto3.client("bedrock-runtime", region_name=get_region(config))


def ensure_text(payload: Dict[str, Any]) -> str:
    return normalize_text(payload.get("text"))
