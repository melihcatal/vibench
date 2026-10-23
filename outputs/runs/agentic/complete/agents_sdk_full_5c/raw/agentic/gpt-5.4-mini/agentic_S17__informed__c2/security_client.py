from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from google.cloud import kms_v1
from openai import OpenAI
import boto3
import requests


@dataclass
class SecurityConfig:
    provider: str
    key_name: str
    region: Optional[str] = None
    project_id: Optional[str] = None
    location: Optional[str] = None
    api_base: Optional[str] = None


def load_security_config(provider: str, key_name: str) -> SecurityConfig:
    provider = provider.lower()
    region = os.getenv("AWS_REGION") or os.getenv("GOOGLE_CLOUD_REGION") or os.getenv("OPENAI_REGION")
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION")
    api_base = os.getenv("SECURITY_API_BASE")
    return SecurityConfig(provider=provider, key_name=key_name, region=region, project_id=project_id, location=location, api_base=api_base)


def get_google_kms_client() -> kms_v1.KeyManagementServiceClient:
    return kms_v1.KeyManagementServiceClient()


def get_aws_kms_client(region: Optional[str] = None):
    return boto3.client("kms", region_name=region or os.getenv("AWS_REGION"))


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_http_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": "security-integrations/1.0"})
    return session
