from __future__ import annotations

import os
from typing import Any

import boto3
from botocore.client import BaseClient
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from openai import OpenAI


def require_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def aws_region() -> str:
    return require_env("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))


def kms_client() -> BaseClient:
    return boto3.client("kms", region_name=aws_region())


def cloudtrail_client() -> BaseClient:
    return boto3.client("cloudtrail", region_name=aws_region())


def aws_account_id(sts_client: BaseClient | None = None) -> str:
    client = sts_client or boto3.client("sts", region_name=aws_region())
    return client.get_caller_identity()["Account"]


def openai_client() -> OpenAI:
    api_key = require_env("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    return OpenAI(api_key=api_key, base_url=base_url)


def new_aesgcm_key() -> bytes:
    return AESGCM.generate_key(bit_length=256)


def aesgcm_encrypt(
    key: bytes, nonce: bytes, plaintext: bytes, aad: bytes | None = None
) -> bytes:
    return AESGCM(key).encrypt(nonce, plaintext, aad)


def aesgcm_decrypt(
    key: bytes, nonce: bytes, ciphertext: bytes, aad: bytes | None = None
) -> bytes:
    return AESGCM(key).decrypt(nonce, ciphertext, aad)


def normalize_kms_key_id(key_id: str) -> str:
    if key_id.startswith("arn:aws:kms:"):
        return key_id
    return key_id.strip()


def ensure_dict(value: Any) -> dict[str, str]:
    if value is None:
        return {}
    return {str(k): str(v) for k, v in dict(value).items()}
