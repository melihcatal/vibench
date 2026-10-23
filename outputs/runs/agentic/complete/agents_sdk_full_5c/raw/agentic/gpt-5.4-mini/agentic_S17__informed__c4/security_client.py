from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3
from botocore.client import BaseClient

from security_models import normalize_text


@dataclass
class SecurityConfig:
    aws_region: str
    kms_key_id: str
    signing_key_id: Optional[str] = None


def load_security_config() -> SecurityConfig:
    return SecurityConfig(
        aws_region=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")),
        kms_key_id=os.environ.get("AWS_KMS_KEY_ID", "alias/app-key"),
        signing_key_id=os.getenv("AWS_KMS_SIGNING_KEY_ID"),
    )


def get_kms_client(region_name: Optional[str] = None) -> BaseClient:
    return boto3.client("kms", region_name=region_name or load_security_config().aws_region)


def encrypt_with_kms(plaintext: str, key_id: str, encryption_context: Optional[Dict[str, str]] = None) -> bytes:
    client = get_kms_client()
    response = client.encrypt(
        KeyId=key_id,
        Plaintext=normalize_text(plaintext).encode("utf-8"),
        EncryptionContext=encryption_context or {},
    )
    return response["CiphertextBlob"]


def decrypt_with_kms(ciphertext_blob: bytes, encryption_context: Optional[Dict[str, str]] = None) -> str:
    client = get_kms_client()
    response = client.decrypt(
        CiphertextBlob=ciphertext_blob,
        EncryptionContext=encryption_context or {},
    )
    plaintext = response["Plaintext"]
    return plaintext.decode("utf-8") if isinstance(plaintext, (bytes, bytearray)) else str(plaintext)


def generate_data_key(key_id: str, key_spec: str = "AES_256", encryption_context: Optional[Dict[str, str]] = None) -> Dict[str, bytes]:
    client = get_kms_client()
    response = client.generate_data_key(
        KeyId=key_id,
        KeySpec=key_spec,
        EncryptionContext=encryption_context or {},
    )
    return {
        "Plaintext": response["Plaintext"],
        "CiphertextBlob": response["CiphertextBlob"],
    }


def sign_with_kms(message: bytes, key_id: Optional[str] = None) -> bytes:
    client = get_kms_client()
    response = client.sign(
        KeyId=key_id or load_security_config().signing_key_id or load_security_config().kms_key_id,
        Message=message,
        MessageType="RAW",
        SigningAlgorithm="RSASSA_PSS_SHA_256",
    )
    return response["Signature"]


def verify_with_kms(message: bytes, signature: bytes, key_id: Optional[str] = None) -> bool:
    client = get_kms_client()
    response = client.verify(
        KeyId=key_id or load_security_config().signing_key_id or load_security_config().kms_key_id,
        Message=message,
        MessageType="RAW",
        Signature=signature,
        SigningAlgorithm="RSASSA_PSS_SHA_256",
    )
    return bool(response.get("SignatureValid", False))


def safe_b64encode(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def safe_b64decode(data: str) -> bytes:
    return base64.b64decode(data.encode("ascii"))
