from __future__ import annotations

import base64
import json
import os
from dataclasses import asdict
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from security_models import (
    AuditNote,
    CryptoEvent,
    EnvelopeCiphertext,
    KeyRequest,
    KeyResponse,
    SafetyFinding,
    SigningRequest,
    SigningResult,
    TranslationRequest,
)

AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")


def load_json_env(name: str, default: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    raw = os.getenv(name)
    if not raw:
        return default or {}
    try:
        parsed = json.loads(raw)
        return parsed if isinstance(parsed, dict) else (default or {})
    except json.JSONDecodeError:
        return default or {}


def encode_bytes(value: bytes) -> str:
    return base64.b64encode(value).decode("utf-8")


def decode_bytes(value: str) -> bytes:
    return base64.b64decode(value.encode("utf-8"))


def kms_client(region_name: Optional[str] = None):
    return boto3.client("kms", region_name=region_name or AWS_DEFAULT_REGION)


def encrypt_with_kms(request: KeyRequest, region_name: Optional[str] = None) -> KeyResponse:
    client = kms_client(region_name)
    response = client.encrypt(
        KeyId=request.key_id,
        Plaintext=request.plaintext.encode("utf-8"),
        EncryptionContext=request.encryption_context or None,
    )
    return KeyResponse(
        key_id=request.key_id,
        ciphertext=encode_bytes(response["CiphertextBlob"]),
        metadata={"encryption_algorithm": response.get("EncryptionAlgorithm")},
    )


def decrypt_with_kms(ciphertext: str, key_id: str, encryption_context: Optional[Dict[str, str]] = None, region_name: Optional[str] = None) -> KeyResponse:
    client = kms_client(region_name)
    response = client.decrypt(
        CiphertextBlob=decode_bytes(ciphertext),
        EncryptionContext=encryption_context or None,
        KeyId=key_id,
    )
    return KeyResponse(
        key_id=key_id,
        plaintext=response["Plaintext"].decode("utf-8"),
        metadata={"encryption_algorithm": response.get("EncryptionAlgorithm")},
    )


def generate_data_key(key_id: str, encryption_context: Optional[Dict[str, str]] = None, region_name: Optional[str] = None) -> Dict[str, str]:
    client = kms_client(region_name)
    response = client.generate_data_key(
        KeyId=key_id,
        KeySpec="AES_256",
        EncryptionContext=encryption_context or None,
    )
    return {
        "plaintext_data_key": encode_bytes(response["Plaintext"]),
        "encrypted_data_key": encode_bytes(response["CiphertextBlob"]),
    }


def sign_with_kms(request: SigningRequest, region_name: Optional[str] = None) -> SigningResult:
    client = kms_client(region_name)
    response = client.sign(
        KeyId=request.key_id,
        Message=request.message,
        MessageType="RAW",
        SigningAlgorithm="RSASSA_PSS_SHA_256",
    )
    return SigningResult(key_id=request.key_id, signature=encode_bytes(response["Signature"]))


def verify_with_kms(request: SigningRequest, signature: str, region_name: Optional[str] = None) -> SigningResult:
    client = kms_client(region_name)
    response = client.verify(
        KeyId=request.key_id,
        Message=request.message,
        MessageType="RAW",
        Signature=decode_bytes(signature),
        SigningAlgorithm="RSASSA_PSS_SHA_256",
    )
    return SigningResult(key_id=request.key_id, signature=signature, verified=response.get("SignatureValid"))


def list_crypto_events(region_name: Optional[str] = None) -> list[CryptoEvent]:
    client = kms_client(region_name)
    events = []
    try:
        paginator = client.get_paginator("list_aliases")
        for page in paginator.paginate():
            for alias in page.get("Aliases", []):
                events.append(
                    CryptoEvent(
                        key_id=alias.get("TargetKeyId", ""),
                        operation="alias",
                        status="listed",
                        details={"alias_name": alias.get("AliasName")},
                    )
                )
    except (BotoCoreError, ClientError):
        return []
    return events


def normalize_envelope(value: Dict[str, Any]) -> EnvelopeCiphertext:
    return EnvelopeCiphertext(
        key_id=value["key_id"],
        encrypted_data_key=value["encrypted_data_key"],
        iv=value["iv"],
        ciphertext=value["ciphertext"],
        tag=value.get("tag"),
        encryption_context=value.get("encryption_context", {}),
    )


def normalize_audit_note(text: str, metadata: Optional[Dict[str, Any]] = None) -> AuditNote:
    metadata = metadata or {}
    labels = metadata.get("labels", [])
    return AuditNote(text=text, labels=labels, metadata=metadata)


def normalize_safety(text: str, unsafe: bool, categories: Optional[list[str]] = None, score: Optional[float] = None) -> SafetyFinding:
    return SafetyFinding(text=text, unsafe=unsafe, categories=categories or [], score=score)


def normalize_translation(text: str, target_language: str, source_language: Optional[str] = None) -> TranslationRequest:
    return TranslationRequest(text=text, target_language=target_language, source_language=source_language)
