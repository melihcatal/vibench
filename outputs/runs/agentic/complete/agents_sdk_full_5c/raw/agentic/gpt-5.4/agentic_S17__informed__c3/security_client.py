from __future__ import annotations

import os
from typing import Optional

import boto3
from botocore.client import BaseClient
from openai import OpenAI


DEFAULT_KMS_REGION = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
DEFAULT_OPENAI_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
DEFAULT_OPENAI_EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")



def get_kms_client(region_name: Optional[str] = None) -> BaseClient:
    return boto3.client("kms", region_name=region_name or DEFAULT_KMS_REGION)



def get_cloudtrail_client(region_name: Optional[str] = None) -> BaseClient:
    return boto3.client("cloudtrail", region_name=region_name or DEFAULT_KMS_REGION)



def get_bedrock_runtime_client(region_name: Optional[str] = None) -> BaseClient:
    return boto3.client("bedrock-runtime", region_name=region_name or DEFAULT_KMS_REGION)



def get_openai_client(api_key: Optional[str] = None) -> OpenAI:
    return OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))



def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value
