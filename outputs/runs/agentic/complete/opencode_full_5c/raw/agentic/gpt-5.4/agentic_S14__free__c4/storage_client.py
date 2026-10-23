from __future__ import annotations

import os

import boto3


def get_aws_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def get_s3_client():
    return boto3.client("s3", region_name=get_aws_region())


def get_s3_bucket(default_bucket: str | None = None) -> str:
    bucket = default_bucket or os.getenv("S3_BUCKET") or os.getenv("AWS_S3_BUCKET")
    if not bucket:
        raise ValueError(
            "S3 bucket is required via argument or S3_BUCKET/AWS_S3_BUCKET"
        )
    return bucket


def get_google_project_id() -> str:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT or GCP_PROJECT is required")
    return project_id


def get_openai_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return api_key
