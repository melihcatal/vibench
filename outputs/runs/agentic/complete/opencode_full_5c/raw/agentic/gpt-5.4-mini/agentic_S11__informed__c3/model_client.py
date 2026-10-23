import os
from typing import Any, Dict, Optional

import boto3


def load_config() -> Dict[str, Any]:
    return {
        "region": os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")),
        "model_id": os.getenv(
            "BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0"
        ),
        "inference_profile_id": os.getenv("BEDROCK_INFERENCE_PROFILE_ID"),
        "guardrail_id": os.getenv("BEDROCK_GUARDRAIL_ID"),
        "guardrail_version": os.getenv("BEDROCK_GUARDRAIL_VERSION"),
    }


def bedrock_client(region: Optional[str] = None):
    return boto3.client(
        "bedrock-runtime", region_name=region or load_config()["region"]
    )


def bedrock_service_client(region: Optional[str] = None):
    return boto3.client("bedrock", region_name=region or load_config()["region"])
