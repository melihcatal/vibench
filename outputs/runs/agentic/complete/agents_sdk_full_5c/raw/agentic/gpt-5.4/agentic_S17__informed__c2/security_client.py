from __future__ import annotations

import os
from typing import Optional

import boto3
from botocore.client import BaseClient
from openai import OpenAI


AWS_REGION_ENV_KEYS = ("AWS_REGION", "AWS_DEFAULT_REGION")


def get_aws_region(default: str = "us-east-1") -> str:
    for key in AWS_REGION_ENV_KEYS:
        value = os.getenv(key)
        if value:
            return value
    return default


def get_kms_key_id(explicit_key_id: Optional[str] = None) -> str:
    key_id = explicit_key_id or os.getenv("AWS_KMS_KEY_ID")
    if not key_id:
        raise ValueError("AWS_KMS_KEY_ID is required")
    return key_id


def get_kms_client(region_name: Optional[str] = None) -> BaseClient:
    return boto3.client("kms", region_name=region_name or get_aws_region())


def get_cloudtrail_client(region_name: Optional[str] = None) -> BaseClient:
    return boto3.client("cloudtrail", region_name=region_name or get_aws_region())


def get_bedrock_runtime_client(region_name: Optional[str] = None) -> BaseClient:
    return boto3.client("bedrock-runtime", region_name=region_name or get_aws_region())


def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return OpenAI(api_key=api_key)


def get_perspective_api_key(explicit_api_key: Optional[str] = None) -> str:
    api_key = explicit_api_key or os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY is required")
    return api_key


def get_deepl_auth_key(explicit_auth_key: Optional[str] = None) -> str:
    auth_key = explicit_auth_key or os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY is required")
    return auth_key
