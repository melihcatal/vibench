from __future__ import annotations

import os

import boto3
from botocore.client import BaseClient
from botocore.config import Config


def get_aws_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def get_s3_client() -> BaseClient:
    endpoint_url = os.getenv("AWS_S3_ENDPOINT_URL")
    session = boto3.session.Session(region_name=get_aws_region())
    return session.client(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
        config=Config(signature_version="s3v4"),
    )


def get_textract_client() -> BaseClient:
    session = boto3.session.Session(region_name=get_aws_region())
    return session.client(
        "textract",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
    )
