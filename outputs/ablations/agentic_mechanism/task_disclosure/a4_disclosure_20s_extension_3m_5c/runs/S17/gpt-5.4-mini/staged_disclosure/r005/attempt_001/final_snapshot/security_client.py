import os
from dataclasses import dataclass
from typing import Optional

import boto3
from botocore.client import BaseClient


@dataclass(frozen=True)
class SecurityConfig:
    aws_region: str
    kms_key_id: Optional[str]


def load_security_config() -> SecurityConfig:
    return SecurityConfig(
        aws_region=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")),
        kms_key_id=os.getenv("AWS_KMS_KEY_ID"),
    )


def create_kms_client(region_name: Optional[str] = None) -> BaseClient:
    config = load_security_config()
    return boto3.client("kms", region_name=region_name or config.aws_region)


def encrypt_bytes(plaintext: bytes, key_id: Optional[str] = None, region_name: Optional[str] = None) -> bytes:
    config = load_security_config()
    kms = create_kms_client(region_name=region_name)
    response = kms.encrypt(KeyId=key_id or config.kms_key_id, Plaintext=plaintext)
    return response["CiphertextBlob"]


def decrypt_bytes(ciphertext: bytes, region_name: Optional[str] = None) -> bytes:
    kms = create_kms_client(region_name=region_name)
    response = kms.decrypt(CiphertextBlob=ciphertext)
    return response["Plaintext"]
