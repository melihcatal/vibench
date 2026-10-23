import os
from functools import lru_cache

import boto3


def _env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name, default)
    return value if value not in ("", None) else default


@lru_cache(maxsize=1)
def bedrock_runtime_client():
    return boto3.client(
        "bedrock-runtime",
        region_name=_env("AWS_REGION", _env("AWS_DEFAULT_REGION", "us-east-1")),
    )


@lru_cache(maxsize=1)
def bedrock_client():
    return boto3.client(
        "bedrock",
        region_name=_env("AWS_REGION", _env("AWS_DEFAULT_REGION", "us-east-1")),
    )


def model_id() -> str:
    return _env("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0")


def inference_profile_arn() -> str | None:
    return _env("BEDROCK_INFERENCE_PROFILE_ARN")


def project_arn() -> str | None:
    return _env("BEDROCK_PROJECT_ARN")
