from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import boto3
from botocore.client import BaseClient

from security_models import coerce_bytes


@dataclass
class SecurityConfig:
    region_name: Optional[str]
    key_id: str
    signing_key_id: Optional[str] = None


def load_security_config() -> SecurityConfig:
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    key_id = os.getenv("AWS_KMS_KEY_ID", "alias/demo-key")
    signing_key_id = os.getenv("AWS_KMS_SIGNING_KEY_ID")
    return SecurityConfig(region_name=region, key_id=key_id, signing_key_id=signing_key_id)


def kms_client(region_name: Optional[str] = None) -> BaseClient:
    config = load_security_config()
    return boto3.client("kms", region_name=region_name or config.region_name)


def kms_key_id() -> str:
    return load_security_config().key_id


def signing_key_id() -> str:
    config = load_security_config()
    return config.signing_key_id or config.key_id


def as_plaintext_bytes(text: object) -> bytes:
    return coerce_bytes(text)
