from __future__ import annotations

import os
from typing import Dict, Optional

import boto3
from botocore.config import Config
from openai import OpenAI
import requests
import deepl


def _aws_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def kms_key_id(explicit_key_id: Optional[str] = None) -> str:
    key_id = explicit_key_id or os.getenv("AWS_KMS_KEY_ID")
    if not key_id:
        raise ValueError("AWS_KMS_KEY_ID is required")
    return key_id


def aws_kms_client():
    return boto3.client(
        "kms",
        region_name=_aws_region(),
        config=Config(retries={"max_attempts": 3, "mode": "standard"}),
    )


def aws_cloudtrail_client():
    return boto3.client(
        "cloudtrail",
        region_name=_aws_region(),
        config=Config(retries={"max_attempts": 3, "mode": "standard"}),
    )


def openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return OpenAI(api_key=api_key)


def perspective_headers() -> Dict[str, str]:
    return {"Content-Type": "application/json"}


def perspective_url() -> str:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY is required")
    return f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"


def perspective_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(perspective_headers())
    return session


def deepl_translator() -> deepl.Translator:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY is required")
    return deepl.Translator(auth_key)
