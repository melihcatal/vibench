import os
from dataclasses import dataclass

import boto3


@dataclass
class SecurityConfig:
    region: str | None = None
    key_id: str | None = None
    signing_key_id: str | None = None


def load_security_config(config=None):
    config = config or {}
    return SecurityConfig(
        region=config.get("region") or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        key_id=config.get("key_id") or os.getenv("AWS_KMS_KEY_ID"),
        signing_key_id=config.get("signing_key_id") or os.getenv("AWS_KMS_SIGNING_KEY_ID"),
    )


def kms_client(config=None):
    security_config = load_security_config(config)
    return boto3.client("kms", region_name=security_config.region), security_config


def normalize_blob(value):
    if value is None:
        return b""
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode("utf-8")
    return bytes(value)
