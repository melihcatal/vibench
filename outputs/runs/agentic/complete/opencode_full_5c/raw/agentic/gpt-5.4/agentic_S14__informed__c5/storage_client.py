from __future__ import annotations

import os

import boto3
from botocore.client import BaseClient
from botocore.config import Config


def get_aws_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def get_s3_client() -> BaseClient:
    session = boto3.session.Session(region_name=get_aws_region())
    endpoint_url = os.getenv("AWS_S3_ENDPOINT_URL")
    addressing_style = os.getenv("AWS_S3_ADDRESSING_STYLE", "auto")
    config = Config(s3={"addressing_style": addressing_style})
    return session.client("s3", endpoint_url=endpoint_url, config=config)


def get_textract_client() -> BaseClient:
    session = boto3.session.Session(region_name=get_aws_region())
    return session.client("textract")


def get_translate_client() -> BaseClient:
    session = boto3.session.Session(region_name=get_aws_region())
    return session.client("translate")
