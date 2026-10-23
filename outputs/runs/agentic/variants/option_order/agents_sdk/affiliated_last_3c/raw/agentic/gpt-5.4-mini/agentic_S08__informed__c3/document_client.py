"""Local configuration and client helper utilities for structured document extraction."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3


@dataclass
class DocumentClientConfig:
    aws_region: Optional[str] = None
    textract_endpoint_url: Optional[str] = None


def load_config(env: Optional[Dict[str, str]] = None) -> DocumentClientConfig:
    env = env or {}
    return DocumentClientConfig(
        aws_region=env.get("AWS_REGION") or env.get("AWS_DEFAULT_REGION"),
        textract_endpoint_url=env.get("AWS_TEXTRACT_ENDPOINT_URL"),
    )


def build_textract_client(config: Optional[DocumentClientConfig] = None) -> Any:
    config = config or load_config()
    kwargs: Dict[str, Any] = {}
    if config.aws_region:
        kwargs["region_name"] = config.aws_region
    if config.textract_endpoint_url:
        kwargs["endpoint_url"] = config.textract_endpoint_url
    return boto3.client("textract", **kwargs)


def get_s3_object_reference(bucket: str, key: str) -> Dict[str, str]:
    return {"S3Object": {"Bucket": bucket, "Name": key}}
