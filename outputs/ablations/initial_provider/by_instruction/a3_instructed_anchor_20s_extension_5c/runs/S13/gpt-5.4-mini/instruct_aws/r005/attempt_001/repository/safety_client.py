import os
from typing import Any, Dict, Optional

import boto3


AWS_REGION_ENV = "AWS_REGION"
AWS_PROFILE_ENV = "AWS_PROFILE"
AWS_ACCESS_KEY_ID_ENV = "AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY_ENV = "AWS_SECRET_ACCESS_KEY"
AWS_SESSION_TOKEN_ENV = "AWS_SESSION_TOKEN"


def load_config() -> Dict[str, Any]:
    return {
        "region": os.getenv(AWS_REGION_ENV, "us-east-1"),
        "profile": os.getenv(AWS_PROFILE_ENV),
        "source_text": os.getenv("SAFETY_SOURCE_TEXT", ""),
        "custom_prompt": os.getenv("SAFETY_CUSTOM_PROMPT", ""),
    }


def _session() -> boto3.session.Session:
    profile = os.getenv(AWS_PROFILE_ENV)
    if profile:
        return boto3.Session(profile_name=profile)
    return boto3.Session()


def bedrock_runtime_client(region: Optional[str] = None):
    cfg = load_config()
    return _session().client("bedrock-runtime", region_name=region or cfg["region"])


def bedrock_client(region: Optional[str] = None):
    cfg = load_config()
    return _session().client("bedrock", region_name=region or cfg["region"])
