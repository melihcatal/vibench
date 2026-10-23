from __future__ import annotations

import os
from typing import Dict, Optional

import boto3
from botocore.config import Config
from openai import OpenAI
import requests
from google.cloud import translate_v2 as translate


DEFAULT_AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
DEFAULT_OPENAI_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini")
DEFAULT_OPENAI_EMBEDDING_MODEL = os.getenv(
    "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
)


def load_encryption_context(extra: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    context = {}
    tenant = os.getenv("SECURITY_TENANT")
    system = os.getenv("SECURITY_SYSTEM", "kms-integration")
    if tenant:
        context["tenant"] = tenant
    if system:
        context["system"] = system
    if extra:
        context.update({k: str(v) for k, v in extra.items()})
    return context


def get_kms_client(region_name: Optional[str] = None):
    return boto3.client(
        "kms",
        region_name=region_name or DEFAULT_AWS_REGION,
        config=Config(retries={"max_attempts": 5, "mode": "standard"}),
    )


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_perspective_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    return session


def get_translate_client() -> translate.Client:
    return translate.Client()
