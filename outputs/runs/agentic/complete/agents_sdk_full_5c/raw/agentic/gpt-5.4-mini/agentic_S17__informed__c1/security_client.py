from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import boto3

from security_models import denormalize_b64, normalize_b64


@dataclass
class SecurityConfig:
    aws_region: str
    kms_key_id: str
    signing_key_id: Optional[str] = None


class SecurityClient:
    def __init__(self, config: Optional[SecurityConfig] = None):
        self.config = config or load_security_config()
        self.kms = boto3.client("kms", region_name=self.config.aws_region)

    def encrypt(self, plaintext: str, key_id: Optional[str] = None, aad: Optional[str] = None) -> str:
        response = self.kms.encrypt(
            KeyId=key_id or self.config.kms_key_id,
            Plaintext=plaintext.encode("utf-8"),
            EncryptionContext={"aad": aad} if aad else None,
        )
        return normalize_b64(response["CiphertextBlob"])

    def decrypt(self, ciphertext_b64: str, aad: Optional[str] = None) -> str:
        response = self.kms.decrypt(
            CiphertextBlob=denormalize_b64(ciphertext_b64),
            EncryptionContext={"aad": aad} if aad else None,
        )
        return response["Plaintext"].decode("utf-8")

    def generate_data_key(self, key_id: Optional[str] = None, key_spec: str = "AES_256"):
        return self.kms.generate_data_key(KeyId=key_id or self.config.kms_key_id, KeySpec=key_spec)

    def sign(self, message: str, signing_key_id: Optional[str] = None) -> str:
        response = self.kms.sign(
            KeyId=signing_key_id or self.config.signing_key_id or self.config.kms_key_id,
            Message=message.encode("utf-8"),
            MessageType="RAW",
            SigningAlgorithm="RSASSA_PSS_SHA_256",
        )
        return normalize_b64(response["Signature"])

    def verify(self, message: str, signature_b64: str, signing_key_id: Optional[str] = None) -> bool:
        response = self.kms.verify(
            KeyId=signing_key_id or self.config.signing_key_id or self.config.kms_key_id,
            Message=message.encode("utf-8"),
            MessageType="RAW",
            Signature=denormalize_b64(signature_b64),
            SigningAlgorithm="RSASSA_PSS_SHA_256",
        )
        return bool(response.get("SignatureValid"))


def load_security_config() -> SecurityConfig:
    return SecurityConfig(
        aws_region=os.environ.get("AWS_REGION", "us-east-1"),
        kms_key_id=os.environ.get("AWS_KMS_KEY_ID", "alias/default-kms-key"),
        signing_key_id=os.environ.get("AWS_KMS_SIGNING_KEY_ID"),
    )
