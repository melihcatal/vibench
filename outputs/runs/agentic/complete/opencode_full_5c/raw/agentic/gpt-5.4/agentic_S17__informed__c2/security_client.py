from __future__ import annotations

import base64
import os
from typing import Dict, Optional

import boto3
from botocore.client import BaseClient
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from security_models import normalize_encryption_context


AWS_KMS_KEY_ID_ENV = "AWS_KMS_KEY_ID"
AWS_REGION_ENV = "AWS_REGION"


def get_aws_region() -> str:
    return os.getenv(AWS_REGION_ENV, os.getenv("AWS_DEFAULT_REGION", "us-east-1"))


def get_kms_key_id(explicit_key_id: Optional[str] = None) -> str:
    key_id = explicit_key_id or os.getenv(AWS_KMS_KEY_ID_ENV)
    if not key_id:
        raise ValueError("Missing AWS KMS key id. Set AWS_KMS_KEY_ID or pass key_id.")
    return key_id


def get_kms_client(region_name: Optional[str] = None) -> BaseClient:
    return boto3.client("kms", region_name=region_name or get_aws_region())


def get_cloudtrail_client(region_name: Optional[str] = None) -> BaseClient:
    return boto3.client("cloudtrail", region_name=region_name or get_aws_region())


def encode_b64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def decode_b64(data: str) -> bytes:
    return base64.b64decode(data.encode("ascii"))


def kms_context(value: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    return normalize_encryption_context(value)


def aesgcm_encrypt(plaintext: bytes, data_key: bytes) -> Dict[str, str]:
    nonce = os.urandom(12)
    ciphertext = AESGCM(data_key).encrypt(nonce, plaintext, None)
    return {
        "nonce": encode_b64(nonce),
        "ciphertext": encode_b64(ciphertext),
    }


def aesgcm_decrypt(ciphertext_b64: str, nonce_b64: str, data_key: bytes) -> bytes:
    ciphertext = decode_b64(ciphertext_b64)
    nonce = decode_b64(nonce_b64)
    return AESGCM(data_key).decrypt(nonce, ciphertext, None)
