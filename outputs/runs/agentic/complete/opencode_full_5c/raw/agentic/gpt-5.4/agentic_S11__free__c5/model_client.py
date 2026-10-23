from __future__ import annotations

import os
from typing import Optional

import boto3

from model_models import PlatformResource


DEFAULT_REGION = (
    os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
)
DEFAULT_MODEL_ID = os.getenv(
    "BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0"
)


def get_bedrock_runtime_client(region_name: Optional[str] = None):
    return boto3.client("bedrock-runtime", region_name=region_name or DEFAULT_REGION)


def get_bedrock_control_client(region_name: Optional[str] = None):
    return boto3.client("bedrock", region_name=region_name or DEFAULT_REGION)


def load_platform_resource() -> PlatformResource:
    return PlatformResource(
        inference_profile_arn=os.getenv("BEDROCK_INFERENCE_PROFILE_ARN"),
        region_name=DEFAULT_REGION,
        model_id=DEFAULT_MODEL_ID,
    )


def resolve_runtime_model_identifier(resource: PlatformResource) -> str:
    return resource.inference_profile_arn or resource.model_id or DEFAULT_MODEL_ID
