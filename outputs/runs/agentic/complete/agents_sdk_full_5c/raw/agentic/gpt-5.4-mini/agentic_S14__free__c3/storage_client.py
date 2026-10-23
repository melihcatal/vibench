from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

import boto3
from botocore.config import Config
from botocore.client import BaseClient


@dataclass(frozen=True)
class StorageSettings:
    aws_region: str
    bucket_name: Optional[str] = None
    endpoint_url: Optional[str] = None
    profile_name: Optional[str] = None


@lru_cache(maxsize=1)
def load_settings() -> StorageSettings:
    return StorageSettings(
        aws_region=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")),
        bucket_name=os.getenv("S3_BUCKET_NAME"),
        endpoint_url=os.getenv("S3_ENDPOINT_URL"),
        profile_name=os.getenv("AWS_PROFILE"),
    )


@lru_cache(maxsize=1)
def get_session() -> boto3.Session:
    settings = load_settings()
    if settings.profile_name:
        return boto3.Session(profile_name=settings.profile_name, region_name=settings.aws_region)
    return boto3.Session(region_name=settings.aws_region)


@lru_cache(maxsize=4)
def get_s3_client() -> BaseClient:
    settings = load_settings()
    return get_session().client(
        "s3",
        region_name=settings.aws_region,
        endpoint_url=settings.endpoint_url,
        config=Config(signature_version="s3v4"),
    )


@lru_cache(maxsize=4)
def get_textract_client() -> BaseClient:
    settings = load_settings()
    return get_session().client("textract", region_name=settings.aws_region, endpoint_url=settings.endpoint_url)


@lru_cache(maxsize=4)
def get_translate_client() -> BaseClient:
    settings = load_settings()
    return get_session().client("translate", region_name=settings.aws_region, endpoint_url=settings.endpoint_url)


@lru_cache(maxsize=4)
def get_comprehend_client() -> BaseClient:
    settings = load_settings()
    return get_session().client("comprehend", region_name=settings.aws_region, endpoint_url=settings.endpoint_url)


@lru_cache(maxsize=4)
def get_bedrock_runtime_client() -> BaseClient:
    settings = load_settings()
    return get_session().client("bedrock-runtime", region_name=settings.aws_region, endpoint_url=settings.endpoint_url)
