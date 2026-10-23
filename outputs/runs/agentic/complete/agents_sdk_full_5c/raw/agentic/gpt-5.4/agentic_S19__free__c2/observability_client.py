from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import boto3
from botocore.config import Config


@dataclass
class ObservabilityConfig:
    aws_region: str
    cloudwatch_namespace: str
    s3_archive_bucket: Optional[str] = None
    bedrock_model_id: str = "anthropic.claude-3-haiku-20240307-v1:0"


def load_config() -> ObservabilityConfig:
    return ObservabilityConfig(
        aws_region=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")),
        cloudwatch_namespace=os.getenv("CLOUDWATCH_NAMESPACE", "AWS/EC2"),
        s3_archive_bucket=os.getenv("S3_ARCHIVE_BUCKET"),
        bedrock_model_id=os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0"),
    )


def cloudwatch_client(region_name: Optional[str] = None):
    cfg = load_config()
    return boto3.client(
        "cloudwatch",
        region_name=region_name or cfg.aws_region,
        config=Config(retries={"max_attempts": 5, "mode": "standard"}),
    )


def bedrock_runtime_client(region_name: Optional[str] = None):
    cfg = load_config()
    return boto3.client(
        "bedrock-runtime",
        region_name=region_name or cfg.aws_region,
        config=Config(retries={"max_attempts": 4, "mode": "standard"}),
    )


def s3_client(region_name: Optional[str] = None):
    cfg = load_config()
    return boto3.client(
        "s3",
        region_name=region_name or cfg.aws_region,
        config=Config(retries={"max_attempts": 5, "mode": "standard"}),
    )
