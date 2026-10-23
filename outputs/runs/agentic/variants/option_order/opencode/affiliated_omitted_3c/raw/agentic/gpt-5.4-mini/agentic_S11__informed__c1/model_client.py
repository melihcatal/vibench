import os
from dataclasses import dataclass

import boto3


@dataclass
class BedrockSettings:
    region: str
    model_id: str
    profile_arn: str | None


def load_settings() -> BedrockSettings:
    return BedrockSettings(
        region=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")),
        model_id=os.getenv(
            "BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0"
        ),
        profile_arn=os.getenv("BEDROCK_INFERENCE_PROFILE_ARN"),
    )


def bedrock_runtime():
    settings = load_settings()
    return boto3.client("bedrock-runtime", region_name=settings.region)


def bedrock_client():
    settings = load_settings()
    return boto3.client("bedrock", region_name=settings.region)
