from __future__ import annotations

import os
from typing import Optional

import boto3
from botocore.client import BaseClient


def get_aws_region(default: str = "us-east-1") -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or default


def get_secrets_manager_client(region_name: Optional[str] = None) -> BaseClient:
    return boto3.client("secretsmanager", region_name=region_name or get_aws_region())


def get_openai_client():
    from openai import OpenAI

    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def get_perspective_api_key() -> str:
    return os.environ["PERSPECTIVE_API_KEY"]


def get_deepl_client():
    import deepl

    return deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
