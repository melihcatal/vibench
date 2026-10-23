import os
from typing import Any, Dict

import boto3


def _env(name: str, default: str = "") -> str:
    value = os.getenv(name, default)
    return value.strip()


def load_observability_config() -> Dict[str, Any]:
    return {
        "aws_region": _env("AWS_REGION", _env("AWS_DEFAULT_REGION", "us-east-1")),
        "cloudwatch_namespace": _env("CLOUDWATCH_NAMESPACE", "AWS/EC2"),
    }


def cloudwatch_client(region_name: str | None = None):
    cfg = load_observability_config()
    return boto3.client("cloudwatch", region_name=region_name or cfg["aws_region"])
