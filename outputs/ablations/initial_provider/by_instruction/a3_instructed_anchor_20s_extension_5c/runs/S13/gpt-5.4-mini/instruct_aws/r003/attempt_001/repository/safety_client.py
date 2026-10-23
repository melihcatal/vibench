import os
from typing import Optional

import boto3


def aws_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def aws_comprehend_client(service_name: str = "comprehend", region_name: Optional[str] = None):
    return boto3.client(service_name, region_name=region_name or aws_region())


def moderation_threshold() -> float:
    return float(os.getenv("SAFETY_THRESHOLD", "0.5"))


def redaction_token() -> str:
    return os.getenv("SAFETY_REDACTION_TOKEN", "[REDACTED]")
