from __future__ import annotations

import os
from typing import Optional

import boto3

from model_models import ResourceSelection


DEFAULT_MODEL_ID = os.getenv(
    "BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0"
)
DEFAULT_REGION = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
DEFAULT_INFERENCE_PROFILE_ARN = os.getenv(
    "BEDROCK_INFERENCE_PROFILE_ARN",
    "arn:aws:bedrock:us-east-1:123456789012:inference-profile/us.anthropic.claude-3-5-sonnet-20240620-v1:0",
)


def get_bedrock_client(region_name: Optional[str] = None):
    return boto3.client("bedrock-runtime", region_name=region_name or DEFAULT_REGION)


def get_bedrock_control_client(region_name: Optional[str] = None):
    return boto3.client("bedrock", region_name=region_name or DEFAULT_REGION)


def default_resource_selection() -> ResourceSelection:
    return ResourceSelection(
        inference_profile_arn=DEFAULT_INFERENCE_PROFILE_ARN,
        model_id=DEFAULT_MODEL_ID,
        region_name=DEFAULT_REGION,
        tags={"source": "managed-model-platform-workflow"},
    )
