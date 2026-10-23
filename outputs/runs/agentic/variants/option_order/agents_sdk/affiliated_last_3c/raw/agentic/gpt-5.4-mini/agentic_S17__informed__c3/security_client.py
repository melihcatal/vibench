from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from security_models import normalize_mapping, normalize_text

AWS_KMS_PROVIDER = "aws-kms"
AWS_BEDROCK_PROVIDER = "aws-bedrock"


@dataclass
class SecurityConfig:
    region_name: Optional[str] = None
    kms_key_id: Optional[str] = None
    signing_key_id: Optional[str] = None
    bedrock_model_id: str = "amazon.titan-embed-text-v2:0"
    translation_source: str = "en"
    translation_target: str = "es"
    moderation_threshold: float = 0.65


def load_config() -> SecurityConfig:
    return SecurityConfig(
        region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        kms_key_id=os.getenv("AWS_KMS_KEY_ID"),
        signing_key_id=os.getenv("AWS_KMS_SIGNING_KEY_ID"),
        bedrock_model_id=os.getenv("BEDROCK_MODEL_ID", "amazon.titan-embed-text-v2:0"),
        translation_source=os.getenv("TRANSLATION_SOURCE_LANG", "en"),
        translation_target=os.getenv("TRANSLATION_TARGET_LANG", "es"),
        moderation_threshold=float(os.getenv("MODERATION_THRESHOLD", "0.65")),
    )


def kms_client(region_name: Optional[str] = None):
    return boto3.client("kms", region_name=region_name or load_config().region_name)


def bedrock_runtime_client(region_name: Optional[str] = None):
    return boto3.client("bedrock-runtime", region_name=region_name or load_config().region_name)


def encrypt_with_kms(plaintext: str, key_id: str, encryption_context: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    client = kms_client()
    response = client.encrypt(
        KeyId=key_id,
        Plaintext=normalize_text(plaintext).encode("utf-8"),
        EncryptionContext=normalize_mapping(encryption_context),
    )
    ciphertext = response["CiphertextBlob"]
    return {
        "provider": AWS_KMS_PROVIDER,
        "key_id": key_id,
        "ciphertext": base64.b64encode(ciphertext).decode("ascii"),
        "arn": response.get("KeyId"),
    }


def decrypt_with_kms(ciphertext_b64: str, key_id: str, encryption_context: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    client = kms_client()
    response = client.decrypt(
        CiphertextBlob=base64.b64decode(ciphertext_b64),
        EncryptionContext=normalize_mapping(encryption_context),
    )
    plaintext = response["Plaintext"].decode("utf-8", errors="replace")
    return {
        "provider": AWS_KMS_PROVIDER,
        "key_id": key_id,
        "plaintext": plaintext,
        "arn": response.get("KeyId"),
    }


def sign_with_kms(message: str, key_id: str) -> Dict[str, Any]:
    client = kms_client()
    response = client.sign(
        KeyId=key_id,
        Message=normalize_text(message).encode("utf-8"),
        MessageType="RAW",
        SigningAlgorithm="RSASSA_PSS_SHA_256",
    )
    return {
        "provider": AWS_KMS_PROVIDER,
        "key_id": key_id,
        "signature": base64.b64encode(response["Signature"]).decode("ascii"),
    }


def verify_with_kms(message: str, signature_b64: str, key_id: str) -> Dict[str, Any]:
    client = kms_client()
    response = client.verify(
        KeyId=key_id,
        Message=normalize_text(message).encode("utf-8"),
        MessageType="RAW",
        Signature=base64.b64decode(signature_b64),
        SigningAlgorithm="RSASSA_PSS_SHA_256",
    )
    return {
        "provider": AWS_KMS_PROVIDER,
        "key_id": key_id,
        "verified": bool(response.get("SignatureValid")),
    }


def envelope_encrypt_payload(plaintext: str, key_id: str, encryption_context: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    data_key = kms_client().generate_data_key(
        KeyId=key_id,
        KeySpec="AES_256",
        EncryptionContext=normalize_mapping(encryption_context),
    )
    plaintext_key = data_key["Plaintext"]
    ciphertext_key = base64.b64encode(data_key["CiphertextBlob"]).decode("ascii")
    return {
        "provider": AWS_KMS_PROVIDER,
        "key_id": key_id,
        "kms_ciphertext_key": ciphertext_key,
        "ciphertext_payload": base64.b64encode(normalize_text(plaintext).encode("utf-8") + b"::" + plaintext_key[:8]).decode("ascii"),
    }
