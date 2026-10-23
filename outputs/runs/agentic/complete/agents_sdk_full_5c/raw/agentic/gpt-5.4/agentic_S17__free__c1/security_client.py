from __future__ import annotations

import os
from typing import Optional

import boto3
from botocore.client import BaseClient
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


DEFAULT_AWS_REGION = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
DEFAULT_KMS_KEY_ID = os.getenv("AWS_KMS_KEY_ID", "")
DEFAULT_BEDROCK_REGION = os.getenv("BEDROCK_AWS_REGION") or DEFAULT_AWS_REGION
DEFAULT_OPENAI_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
DEFAULT_DEEPL_MODEL_TYPE = os.getenv("DEEPL_MODEL_TYPE", "prefer_quality_optimized")


def get_kms_client(region_name: Optional[str] = None) -> BaseClient:
    return boto3.client("kms", region_name=region_name or DEFAULT_AWS_REGION)


def get_cloudtrail_client(region_name: Optional[str] = None) -> BaseClient:
    return boto3.client("cloudtrail", region_name=region_name or DEFAULT_AWS_REGION)


def get_bedrock_runtime_client(region_name: Optional[str] = None) -> BaseClient:
    return boto3.client("bedrock-runtime", region_name=region_name or DEFAULT_BEDROCK_REGION)


def get_aesgcm(key_bytes: bytes) -> AESGCM:
    return AESGCM(key_bytes)
