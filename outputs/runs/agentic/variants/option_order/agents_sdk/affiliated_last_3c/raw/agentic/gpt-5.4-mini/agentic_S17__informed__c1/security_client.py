from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3
from botocore.client import BaseClient

from security_models import CiphertextResponse, NormalizedResult, SignRequest, VerifyRequest, normalize_bytes, normalize_mapping

AWS_REGION_ENV = "AWS_REGION"
AWS_DEFAULT_REGION_ENV = "AWS_DEFAULT_REGION"
AWS_ACCESS_KEY_ENV = "AWS_ACCESS_KEY_ID"
AWS_SECRET_KEY_ENV = "AWS_SECRET_ACCESS_KEY"


@dataclass
class SecurityConfig:
    region_name: Optional[str] = None
    kms_key_id: Optional[str] = None
    signing_key_id: Optional[str] = None
    provider: str = "aws-kms"


def load_security_config() -> SecurityConfig:
    return SecurityConfig(
        region_name=os.getenv(AWS_REGION_ENV) or os.getenv(AWS_DEFAULT_REGION_ENV),
        kms_key_id=os.getenv("KMS_KEY_ID"),
        signing_key_id=os.getenv("KMS_SIGNING_KEY_ID"),
    )


def get_kms_client(region_name: Optional[str] = None) -> BaseClient:
    config = load_security_config()
    region = region_name or config.region_name or "us-east-1"
    return boto3.client("kms", region_name=region)


def encrypt_with_kms(key_id: str, plaintext: bytes, aad: bytes = b"") -> CiphertextResponse:
    client = get_kms_client()
    response = client.encrypt(
        KeyId=key_id,
        Plaintext=normalize_bytes(plaintext),
        EncryptionContext={"aad": base64.b64encode(normalize_bytes(aad)).decode("ascii")} if aad else {},
    )
    return CiphertextResponse(
        key_id=key_id,
        ciphertext=normalize_bytes(response["CiphertextBlob"]),
        metadata=normalize_mapping(response),
    )


def decrypt_with_kms(key_id: str, ciphertext: bytes, aad: bytes = b"") -> CiphertextResponse:
    client = get_kms_client()
    response = client.decrypt(
        KeyId=key_id,
        CiphertextBlob=normalize_bytes(ciphertext),
        EncryptionContext={"aad": base64.b64encode(normalize_bytes(aad)).decode("ascii")} if aad else {},
    )
    return CiphertextResponse(
        key_id=key_id,
        ciphertext=normalize_bytes(response["Plaintext"]),
        metadata=normalize_mapping(response),
    )


def sign_with_kms(request: SignRequest) -> NormalizedResult:
    client = get_kms_client()
    response = client.sign(
        KeyId=request.key_id,
        Message=normalize_bytes(request.message),
        MessageType="RAW",
        SigningAlgorithm=request.algorithm,
    )
    return NormalizedResult(
        ok=True,
        provider="AWS KMS",
        key_id=request.key_id,
        payload={"signature": base64.b64encode(normalize_bytes(response["Signature"])).decode("ascii")},
        error=None,
    )


def verify_with_kms(request: VerifyRequest) -> NormalizedResult:
    client = get_kms_client()
    response = client.verify(
        KeyId=request.key_id,
        Message=normalize_bytes(request.message),
        MessageType="RAW",
        Signature=normalize_bytes(request.signature),
        SigningAlgorithm=request.algorithm,
    )
    return NormalizedResult(
        ok=bool(response.get("SignatureValid", False)),
        provider="AWS KMS",
        key_id=request.key_id,
        payload=normalize_mapping(response),
        error=None if response.get("SignatureValid", False) else "Signature verification failed",
    )
