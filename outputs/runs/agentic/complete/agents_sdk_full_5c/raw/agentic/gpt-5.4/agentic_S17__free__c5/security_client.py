from __future__ import annotations

import os
from typing import Optional

import boto3
from botocore.client import BaseClient
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from openai import OpenAI


AWS_REGION_ENV = "AWS_REGION"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
DEFAULT_KMS_SIGNING_ALGORITHM = "RSASSA_PSS_SHA_256"
DEFAULT_OPENAI_EMBED_MODEL = "text-embedding-3-small"
DEFAULT_OPENAI_MODERATION_MODEL = "omni-moderation-latest"
DEFAULT_OPENAI_TRANSLATION_MODEL = "gpt-4o-mini"


def get_aws_region(explicit_region: Optional[str] = None) -> str:
    return explicit_region or os.getenv(AWS_REGION_ENV, "us-east-1")


def get_kms_client(region_name: Optional[str] = None) -> BaseClient:
    return boto3.client("kms", region_name=get_aws_region(region_name))


def get_cloudtrail_client(region_name: Optional[str] = None) -> BaseClient:
    return boto3.client("cloudtrail", region_name=get_aws_region(region_name))


def get_openai_client(api_key: Optional[str] = None) -> OpenAI:
    return OpenAI(api_key=api_key or os.getenv(OPENAI_API_KEY_ENV))


def build_aesgcm(key_bytes: bytes) -> AESGCM:
    return AESGCM(key_bytes)
