from __future__ import annotations

import base64
import os
from dataclasses import asdict
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from security_models import (
    CryptoEvent,
    DecryptionRequest,
    EncryptionRequest,
    EnvelopeEncryptionRequest,
    NormalizedPayload,
    SignOrVerifyRequest,
)


AWS_KMS_PROVIDER = "AWS Key Management Service"


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default)


def load_configuration() -> Dict[str, str]:
    return {
        "aws_region": _env("AWS_REGION", _env("AWS_DEFAULT_REGION", "us-east-1")),
        "kms_key_id": _env("AWS_KMS_KEY_ID"),
        "signing_key_id": _env("AWS_KMS_SIGNING_KEY_ID", _env("AWS_KMS_KEY_ID")),
    }


def normalize_text_payload(payload: Any) -> NormalizedPayload:
    if isinstance(payload, bytes):
        text = payload.decode("utf-8", errors="replace")
    else:
        text = str(payload)
    return NormalizedPayload(text=text.strip())


def get_kms_client(region_name: Optional[str] = None):
    cfg = load_configuration()
    return boto3.client("kms", region_name=region_name or cfg["aws_region"])


def encrypt_with_kms(req: EncryptionRequest, region_name: Optional[str] = None) -> Dict[str, Any]:
    client = get_kms_client(region_name)
    kwargs: Dict[str, Any] = {"KeyId": req.key_id, "Plaintext": req.plaintext.encode("utf-8")}
    if req.aad:
        kwargs["EncryptionContext"] = {"aad": req.aad}
    resp = client.encrypt(**kwargs)
    return {
        "provider": AWS_KMS_PROVIDER,
        "key_id": req.key_id,
        "ciphertext_blob": base64.b64encode(resp["CiphertextBlob"]).decode("ascii"),
        "key_id_returned": resp.get("KeyId"),
    }


def decrypt_with_kms(req: DecryptionRequest, region_name: Optional[str] = None) -> Dict[str, Any]:
    client = get_kms_client(region_name)
    kwargs: Dict[str, Any] = {"CiphertextBlob": base64.b64decode(req.ciphertext)}
    if req.key_id:
        kwargs["KeyId"] = req.key_id
    if req.aad:
        kwargs["EncryptionContext"] = {"aad": req.aad}
    resp = client.decrypt(**kwargs)
    return {
        "provider": AWS_KMS_PROVIDER,
        "key_id": resp.get("KeyId", req.key_id),
        "plaintext": resp["Plaintext"].decode("utf-8", errors="replace"),
    }


def generate_data_key(req: EnvelopeEncryptionRequest, region_name: Optional[str] = None) -> Dict[str, Any]:
    client = get_kms_client(region_name)
    kwargs: Dict[str, Any] = {"KeyId": req.key_id, "KeySpec": "AES_256"}
    if req.aad:
        kwargs["EncryptionContext"] = {"aad": req.aad}
    resp = client.generate_data_key(**kwargs)
    return {
        "provider": AWS_KMS_PROVIDER,
        "key_id": req.key_id,
        "plaintext_data_key": base64.b64encode(resp["Plaintext"]).decode("ascii"),
        "encrypted_data_key": base64.b64encode(resp["CiphertextBlob"]).decode("ascii"),
    }


def sign_message(req: SignOrVerifyRequest, region_name: Optional[str] = None) -> Dict[str, Any]:
    client = get_kms_client(region_name)
    resp = client.sign(
        KeyId=req.key_id,
        Message=req.message.encode("utf-8"),
        MessageType="RAW",
        SigningAlgorithm="RSASSA_PSS_SHA_256",
    )
    return {
        "provider": AWS_KMS_PROVIDER,
        "key_id": req.key_id,
        "signature": base64.b64encode(resp["Signature"]).decode("ascii"),
        "signing_algorithm": resp.get("SigningAlgorithm", "RSASSA_PSS_SHA_256"),
    }


def verify_signature(req: SignOrVerifyRequest, region_name: Optional[str] = None) -> Dict[str, Any]:
    if not req.signature:
        raise ValueError("signature is required for verification")
    client = get_kms_client(region_name)
    resp = client.verify(
        KeyId=req.key_id,
        Message=req.message.encode("utf-8"),
        MessageType="RAW",
        Signature=base64.b64decode(req.signature),
        SigningAlgorithm="RSASSA_PSS_SHA_256",
    )
    return {
        "provider": AWS_KMS_PROVIDER,
        "key_id": req.key_id,
        "signature_valid": bool(resp.get("SignatureValid", False)),
    }


def crypto_event(operation: str, key_id: str, subject: str, status: str, **details: Any) -> Dict[str, Any]:
    return asdict(CryptoEvent(key_id=key_id, operation=operation, subject=subject, status=status, details=details))


def aws_error_message(exc: Exception) -> str:
    if isinstance(exc, (BotoCoreError, ClientError)):
        return str(exc)
    return f"{type(exc).__name__}: {exc}"
