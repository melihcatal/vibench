from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import boto3


@dataclass(frozen=True)
class PlatformConfig:
    aws_region: str
    bedrock_model_id: str
    guardrail_identifier: Optional[str] = None
    guardrail_version: Optional[str] = None
    translation_target_locale: str = "es"
    embedding_model_id: str = "amazon.titan-embed-text-v2:0"
    tts_voice_id: str = "Joanna"


def load_config() -> PlatformConfig:
    return PlatformConfig(
        aws_region=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")),
        bedrock_model_id=os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0"),
        guardrail_identifier=os.getenv("BEDROCK_GUARDRAIL_IDENTIFIER"),
        guardrail_version=os.getenv("BEDROCK_GUARDRAIL_VERSION"),
        translation_target_locale=os.getenv("TRANSLATION_TARGET_LOCALE", "es"),
        embedding_model_id=os.getenv("BEDROCK_EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v2:0"),
        tts_voice_id=os.getenv("POLLY_VOICE_ID", "Joanna"),
    )


def bedrock_runtime_client():
    config = load_config()
    return boto3.client("bedrock-runtime", region_name=config.aws_region)


def bedrock_client():
    config = load_config()
    return boto3.client("bedrock", region_name=config.aws_region)
