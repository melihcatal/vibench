from __future__ import annotations

import os
from typing import Optional

import boto3
from botocore.client import BaseClient
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from openai import OpenAI


AWS_KMS_PROVIDER = "aws-kms"
OPENAI_PROVIDER = "openai"
OPENAI_EMBED_MODEL = "text-embedding-3-small"
OPENAI_TRANSLATION_MODEL = "gpt-4o-mini"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def get_aws_region(explicit_region: Optional[str] = None) -> str:
    return (
        explicit_region
        or os.getenv("AWS_REGION")
        or os.getenv("AWS_DEFAULT_REGION")
        or "us-east-1"
    )


def get_kms_client(region_name: Optional[str] = None) -> BaseClient:
    return boto3.client("kms", region_name=get_aws_region(region_name))


def get_cloudtrail_client(region_name: Optional[str] = None) -> BaseClient:
    return boto3.client("cloudtrail", region_name=get_aws_region(region_name))


def get_openai_client() -> OpenAI:
    api_key = os.environ["OPENAI_API_KEY"]
    return OpenAI(api_key=api_key)


def kms_encryption_context(aad: Optional[bytes]) -> Optional[dict[str, str]]:
    if aad is None:
        return None
    return {"aad": aad.decode("utf-8")}


def build_aesgcm_cipher(key_bytes: bytes) -> AESGCM:
    return AESGCM(key_bytes)
