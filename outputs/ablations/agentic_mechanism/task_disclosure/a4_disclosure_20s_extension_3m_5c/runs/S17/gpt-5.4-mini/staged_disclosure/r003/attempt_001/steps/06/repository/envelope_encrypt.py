import base64
import os
from dataclasses import dataclass
from typing import Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


@dataclass
class EnvelopeCiphertext:
    encrypted_data_key: str
    nonce: str
    ciphertext: str


def _kms_client():
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    if region:
        return boto3.client("kms", region_name=region)
    return boto3.client("kms")


def encrypt(plaintext: bytes, key_id: Optional[str] = None, aad: Optional[bytes] = None) -> EnvelopeCiphertext:
    if not plaintext:
        raise ValueError("plaintext must not be empty")
    kms = _kms_client()
    response = kms.generate_data_key(KeyId=key_id, KeySpec="AES_256") if key_id else kms.generate_data_key(KeySpec="AES_256")
    data_key_plaintext = response["Plaintext"]
    encrypted_data_key = response["CiphertextBlob"]
    nonce = os.urandom(12)
    aesgcm = AESGCM(data_key_plaintext)
    ciphertext = aesgcm.encrypt(nonce, plaintext, aad)
    return EnvelopeCiphertext(
        encrypted_data_key=base64.b64encode(encrypted_data_key).decode("utf-8"),
        nonce=base64.b64encode(nonce).decode("utf-8"),
        ciphertext=base64.b64encode(ciphertext).decode("utf-8"),
    )


def decrypt(package: EnvelopeCiphertext, aad: Optional[bytes] = None) -> bytes:
    kms = _kms_client()
    encrypted_data_key = base64.b64decode(package.encrypted_data_key)
    nonce = base64.b64decode(package.nonce)
    ciphertext = base64.b64decode(package.ciphertext)
    response = kms.decrypt(CiphertextBlob=encrypted_data_key)
    data_key_plaintext = response["Plaintext"]
    aesgcm = AESGCM(data_key_plaintext)
    return aesgcm.decrypt(nonce, ciphertext, aad)


def _handle_kms_errors(exc: Exception) -> Exception:
    if isinstance(exc, (BotoCoreError, ClientError)):
        return RuntimeError(f"AWS KMS error: {exc}")
    return exc


__all__ = ["EnvelopeCiphertext", "encrypt", "decrypt"]
