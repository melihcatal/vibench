from __future__ import annotations

import os
from typing import Optional

import boto3
from openai import OpenAI


def get_aws_region(explicit_region: Optional[str] = None) -> str:
    return (
        explicit_region
        or os.getenv("AWS_REGION")
        or os.getenv("AWS_DEFAULT_REGION")
        or "us-east-1"
    )


def get_kms_client(region_name: Optional[str] = None):
    return boto3.client("kms", region_name=get_aws_region(region_name))


def get_cloudtrail_client(region_name: Optional[str] = None):
    return boto3.client("cloudtrail", region_name=get_aws_region(region_name))


def get_translate_client(region_name: Optional[str] = None):
    return boto3.client("translate", region_name=get_aws_region(region_name))


def get_openai_client(
    api_key: Optional[str] = None, base_url: Optional[str] = None
) -> OpenAI:
    resolved_key = api_key or os.getenv("OPENAI_API_KEY")
    resolved_base = (
        base_url or os.getenv("OPENAI_BASE_URL") or "https://api.openai.com/v1"
    )
    return OpenAI(api_key=resolved_key, base_url=resolved_base)
