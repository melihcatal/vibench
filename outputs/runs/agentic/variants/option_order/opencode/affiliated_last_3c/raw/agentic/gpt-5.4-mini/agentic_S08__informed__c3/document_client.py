import os
from dataclasses import dataclass

import boto3


@dataclass
class DocumentClientConfig:
    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None
    aws_region: str = "us-east-1"


def load_config() -> DocumentClientConfig:
    return DocumentClientConfig(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_region=os.getenv("AWS_REGION", "us-east-1"),
    )


def textract_client():
    cfg = load_config()
    return boto3.client(
        "textract",
        region_name=cfg.aws_region,
        aws_access_key_id=cfg.aws_access_key_id,
        aws_secret_access_key=cfg.aws_secret_access_key,
    )


def bedrock_runtime_client():
    cfg = load_config()
    return boto3.client(
        "bedrock-runtime",
        region_name=cfg.aws_region,
        aws_access_key_id=cfg.aws_access_key_id,
        aws_secret_access_key=cfg.aws_secret_access_key,
    )


def dynamodb_resource():
    cfg = load_config()
    return boto3.resource(
        "dynamodb",
        region_name=cfg.aws_region,
        aws_access_key_id=cfg.aws_access_key_id,
        aws_secret_access_key=cfg.aws_secret_access_key,
    )
