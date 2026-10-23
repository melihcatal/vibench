import os
from dataclasses import dataclass

import boto3


@dataclass(frozen=True)
class PlatformConfig:
    region: str
    model_id: str
    profile_arn: str


def load_platform_config() -> PlatformConfig:
    return PlatformConfig(
        region=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")),
        model_id=os.getenv(
            "BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0"
        ),
        profile_arn=os.getenv("BEDROCK_INFERENCE_PROFILE_ARN", ""),
    )


def bedrock_runtime_client():
    cfg = load_platform_config()
    return boto3.client("bedrock-runtime", region_name=cfg.region)


def bedrock_client():
    cfg = load_platform_config()
    return boto3.client("bedrock", region_name=cfg.region)
