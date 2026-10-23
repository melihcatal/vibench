from __future__ import annotations

import os
from functools import lru_cache

import boto3
from botocore.client import BaseClient
from openai import OpenAI


AWS_REGION_ENV = "AWS_REGION"
S3_BUCKET_ENV = "S3_BUCKET"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"


def get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None or value == "":
        raise ValueError(f"Missing required environment variable: {name}")
    return value


@lru_cache(maxsize=1)
def get_aws_region() -> str:
    return get_env(AWS_REGION_ENV, os.getenv("AWS_DEFAULT_REGION", "us-east-1"))


@lru_cache(maxsize=1)
def get_default_bucket() -> str:
    return get_env(S3_BUCKET_ENV)


@lru_cache(maxsize=1)
def get_s3_client() -> BaseClient:
    return boto3.client("s3", region_name=get_aws_region())


@lru_cache(maxsize=1)
def get_textract_client() -> BaseClient:
    return boto3.client("textract", region_name=get_aws_region())


@lru_cache(maxsize=1)
def get_translate_client() -> BaseClient:
    return boto3.client("translate", region_name=get_aws_region())


@lru_cache(maxsize=1)
def get_bedrock_runtime_client() -> BaseClient:
    return boto3.client("bedrock-runtime", region_name=get_aws_region())


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    return OpenAI(api_key=get_env(OPENAI_API_KEY_ENV))
