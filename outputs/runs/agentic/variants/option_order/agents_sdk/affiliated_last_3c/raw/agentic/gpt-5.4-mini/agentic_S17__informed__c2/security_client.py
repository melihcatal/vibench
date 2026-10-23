from __future__ import annotations

import base64
import hashlib
import os
from dataclasses import dataclass
from typing import Optional

import boto3
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from botocore.exceptions import BotoCoreError, ClientError

from security_models import normalize_bytes

AWS_KMS_KEY_ID_ENV = "AWS_KMS_KEY_ID"
AWS_REGION_ENV = "AWS_REGION"


@dataclass
class SecurityConfig:
    key_id: str
    region: str


class SecurityClientError(RuntimeError):
    pass


class KmsSecurityClient:
    def __init__(self, config: Optional[SecurityConfig] = None):
        self.config = config or load_config()
        self._kms = boto3.client("kms", region_name=self.config.region)

    def encrypt(self, plaintext: bytes, aad: Optional[bytes] = None) -> bytes:
        try:
            resp = self._kms.encrypt(KeyId=self.config.key_id, Plaintext=plaintext, EncryptionAlgorithm="SYMMETRIC_DEFAULT")
            return resp["CiphertextBlob"]
        except (BotoCoreError, ClientError) as exc:
            raise SecurityClientError(str(exc)) from exc

    def decrypt(self, ciphertext: bytes) -> bytes:
        try:
            resp = self._kms.decrypt(CiphertextBlob=ciphertext, EncryptionAlgorithm="SYMMETRIC_DEFAULT")
            return resp["Plaintext"]
        except (BotoCoreError, ClientError) as exc:
            raise SecurityClientError(str(exc)) from exc

    def generate_data_key(self, key_spec: str = "AES_256"):
        try:
            return self._kms.generate_data_key(KeyId=self.config.key_id, KeySpec=key_spec)
        except (BotoCoreError, ClientError) as exc:
            raise SecurityClientError(str(exc)) from exc

    def sign(self, message: bytes) -> bytes:
        try:
            resp = self._kms.sign(
                KeyId=self.config.key_id,
                Message=message,
                MessageType="RAW",
                SigningAlgorithm="RSASSA_PSS_SHA_256",
            )
            return resp["Signature"]
        except (BotoCoreError, ClientError) as exc:
            raise SecurityClientError(str(exc)) from exc

    def verify(self, message: bytes, signature: bytes) -> bool:
        try:
            resp = self._kms.verify(
                KeyId=self.config.key_id,
                Message=message,
                MessageType="RAW",
                Signature=signature,
                SigningAlgorithm="RSASSA_PSS_SHA_256",
            )
            return bool(resp.get("SignatureValid", False))
        except (BotoCoreError, ClientError) as exc:
            raise SecurityClientError(str(exc)) from exc


def load_config() -> SecurityConfig:
    key_id = os.environ.get(AWS_KMS_KEY_ID_ENV, "alias/default-kms-key")
    region = os.environ.get(AWS_REGION_ENV, "us-east-1")
    return SecurityConfig(key_id=key_id, region=region)


def encrypt_payload(plaintext: str | bytes) -> str:
    client = KmsSecurityClient()
    blob = client.encrypt(normalize_bytes(plaintext) or b"")
    return base64.b64encode(blob).decode("ascii")


def decrypt_payload(ciphertext_b64: str) -> str:
    client = KmsSecurityClient()
    plaintext = client.decrypt(base64.b64decode(ciphertext_b64))
    return plaintext.decode("utf-8", errors="replace")


def envelope_encrypt(plaintext: str | bytes, aad: str | bytes | None = None) -> dict:
    client = KmsSecurityClient()
    data_key = client.generate_data_key()
    raw_key = data_key["Plaintext"]
    cipher = AES.new(raw_key, AES.MODE_GCM)
    if aad is not None:
        cipher.update(normalize_bytes(aad) or b"")
    ct, tag = cipher.encrypt_and_digest(normalize_bytes(plaintext) or b"")
    return {
        "wrapped_data_key": base64.b64encode(data_key["CiphertextBlob"]).decode("ascii"),
        "nonce": base64.b64encode(cipher.nonce).decode("ascii"),
        "ciphertext": base64.b64encode(ct).decode("ascii"),
        "tag": base64.b64encode(tag).decode("ascii"),
    }


def sign_or_verify(message: str | bytes, signature_b64: str | None = None) -> dict:
    client = KmsSecurityClient()
    message_bytes = normalize_bytes(message) or b""
    if signature_b64:
        return {"verified": client.verify(message_bytes, base64.b64decode(signature_b64))}
    signature = client.sign(message_bytes)
    return {"signature": base64.b64encode(signature).decode("ascii")}
