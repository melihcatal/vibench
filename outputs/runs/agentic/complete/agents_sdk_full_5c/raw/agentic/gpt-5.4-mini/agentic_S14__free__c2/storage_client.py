from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

import boto3
from botocore.client import BaseClient
from botocore.config import Config


@dataclass(frozen=True)
class StorageConfig:
    bucket: str
    region_name: str
    access_key_id: Optional[str]
    secret_access_key: Optional[str]
    session_token: Optional[str]
    endpoint_url: Optional[str]


@lru_cache(maxsize=1)
def load_storage_config() -> StorageConfig:
    return StorageConfig(
        bucket=os.environ.get("S3_BUCKET", os.environ.get("AWS_S3_BUCKET", "")),
        region_name=os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1")),
        access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        session_token=os.environ.get("AWS_SESSION_TOKEN"),
        endpoint_url=os.environ.get("AWS_S3_ENDPOINT_URL"),
    )


@lru_cache(maxsize=1)
def get_s3_client() -> BaseClient:
    cfg = load_storage_config()
    session = boto3.session.Session(
        aws_access_key_id=cfg.access_key_id,
        aws_secret_access_key=cfg.secret_access_key,
        aws_session_token=cfg.session_token,
        region_name=cfg.region_name,
    )
    return session.client(
        "s3",
        endpoint_url=cfg.endpoint_url,
        config=Config(signature_version="s3v4"),
    )


@lru_cache(maxsize=1)
def get_textract_client():
    cfg = load_storage_config()
    session = boto3.session.Session(
        aws_access_key_id=cfg.access_key_id,
        aws_secret_access_key=cfg.secret_access_key,
        aws_session_token=cfg.session_token,
        region_name=cfg.region_name,
    )
    return session.client("textract", endpoint_url=cfg.endpoint_url)


@lru_cache(maxsize=1)
def get_translate_client():
    cfg = load_storage_config()
    session = boto3.session.Session(
        aws_access_key_id=cfg.access_key_id,
        aws_secret_access_key=cfg.secret_access_key,
        aws_session_token=cfg.session_token,
        region_name=cfg.region_name,
    )
    return session.client("translate", endpoint_url=cfg.endpoint_url)


@lru_cache(maxsize=1)
def get_bedrock_runtime_client():
    cfg = load_storage_config()
    session = boto3.session.Session(
        aws_access_key_id=cfg.access_key_id,
        aws_secret_access_key=cfg.secret_access_key,
        aws_session_token=cfg.session_token,
        region_name=cfg.region_name,
    )
    return session.client("bedrock-runtime", endpoint_url=cfg.endpoint_url)
