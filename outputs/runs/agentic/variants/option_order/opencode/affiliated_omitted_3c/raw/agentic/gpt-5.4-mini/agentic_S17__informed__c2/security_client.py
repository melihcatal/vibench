import os
from typing import Any, Dict, Optional

import boto3


def _kms_client():
    return boto3.client("kms")


def get_key_id(default: str = "alias/app-key") -> str:
    return os.getenv("AWS_KMS_KEY_ID", default)


def get_aad() -> Dict[str, str]:
    raw = os.getenv("AWS_KMS_ENCRYPTION_CONTEXT", "")
    context: Dict[str, str] = {}
    if raw:
        for item in raw.split(","):
            if "=" in item:
                k, v = item.split("=", 1)
                context[k.strip()] = v.strip()
    return context


def encrypt(
    plaintext: bytes,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    client = _kms_client()
    response = client.encrypt(
        KeyId=key_id or get_key_id(),
        Plaintext=plaintext,
        EncryptionContext=encryption_context or None,
    )
    return response


def decrypt(
    ciphertext_blob: bytes,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    client = _kms_client()
    kwargs: Dict[str, Any] = {"CiphertextBlob": ciphertext_blob}
    if encryption_context:
        kwargs["EncryptionContext"] = encryption_context
    response = client.decrypt(**kwargs)
    return response


def generate_data_key(
    key_id: Optional[str] = None,
    key_spec: str = "AES_256",
    encryption_context: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    client = _kms_client()
    kwargs: Dict[str, Any] = {"KeyId": key_id or get_key_id(), "KeySpec": key_spec}
    if encryption_context:
        kwargs["EncryptionContext"] = encryption_context
    return client.generate_data_key(**kwargs)


def sign(
    message: bytes,
    key_id: Optional[str] = None,
    signing_algorithm: str = "RSASSA_PSS_SHA_256",
) -> Dict[str, Any]:
    client = _kms_client()
    return client.sign(
        KeyId=key_id or get_key_id(),
        Message=message,
        MessageType="RAW",
        SigningAlgorithm=signing_algorithm,
    )


def verify(
    message: bytes,
    signature: bytes,
    key_id: Optional[str] = None,
    signing_algorithm: str = "RSASSA_PSS_SHA_256",
) -> Dict[str, Any]:
    client = _kms_client()
    return client.verify(
        KeyId=key_id or get_key_id(),
        Message=message,
        MessageType="RAW",
        Signature=signature,
        SigningAlgorithm=signing_algorithm,
    )
