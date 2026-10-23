import base64
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3
from botocore.client import BaseClient
from botocore.exceptions import BotoCoreError, ClientError


@dataclass(frozen=True)
class SecurityConfig:
    region_name: str
    kms_key_id: Optional[str] = None
    encryption_context: Optional[Dict[str, str]] = None


def load_security_config() -> SecurityConfig:
    region_name = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    kms_key_id = os.getenv("KMS_KEY_ID") or os.getenv("AWS_KMS_KEY_ID")
    encryption_context_raw = os.getenv("KMS_ENCRYPTION_CONTEXT")
    encryption_context = None
    if encryption_context_raw:
        parsed = json.loads(encryption_context_raw)
        if not isinstance(parsed, dict):
            raise ValueError("KMS_ENCRYPTION_CONTEXT must be a JSON object")
        encryption_context = {str(k): str(v) for k, v in parsed.items()}
    return SecurityConfig(region_name=region_name, kms_key_id=kms_key_id, encryption_context=encryption_context)


def create_kms_client(region_name: Optional[str] = None) -> BaseClient:
    config = load_security_config()
    return boto3.client("kms", region_name=region_name or config.region_name)


def encrypt_bytes(plaintext: bytes, key_id: Optional[str] = None, encryption_context: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    config = load_security_config()
    client = create_kms_client()
    response = client.encrypt(
        KeyId=key_id or config.kms_key_id,
        Plaintext=plaintext,
        EncryptionContext=encryption_context or config.encryption_context or {},
    )
    return {
        "ciphertext_blob": base64.b64encode(response["CiphertextBlob"]).decode("utf-8"),
        "key_id": response.get("KeyId"),
        "encryption_algorithm": response.get("EncryptionAlgorithm"),
    }


def decrypt_bytes(ciphertext_blob_b64: str, encryption_context: Optional[Dict[str, str]] = None) -> bytes:
    client = create_kms_client()
    response = client.decrypt(
        CiphertextBlob=base64.b64decode(ciphertext_blob_b64),
        EncryptionContext=encryption_context or load_security_config().encryption_context or {},
    )
    return response["Plaintext"]


def generate_data_key(key_id: Optional[str] = None, key_spec: str = "AES_256") -> Dict[str, Any]:
    config = load_security_config()
    client = create_kms_client()
    response = client.generate_data_key(
        KeyId=key_id or config.kms_key_id,
        KeySpec=key_spec,
        EncryptionContext=config.encryption_context or {},
    )
    return {
        "plaintext_key": base64.b64encode(response["Plaintext"]).decode("utf-8"),
        "ciphertext_key": base64.b64encode(response["CiphertextBlob"]).decode("utf-8"),
        "key_id": response.get("KeyId"),
    }


def describe_key(key_id: Optional[str] = None) -> Dict[str, Any]:
    client = create_kms_client()
    response = client.describe_key(KeyId=key_id or load_security_config().kms_key_id)
    return response["KeyMetadata"]


def validate_security_configuration() -> None:
    config = load_security_config()
    if not config.kms_key_id:
        raise ValueError("KMS key id must be set via KMS_KEY_ID or AWS_KMS_KEY_ID")
    if not config.region_name:
        raise ValueError("AWS region must be configured")


def encrypt_text(plaintext: str, key_id: Optional[str] = None, encryption_context: Optional[Dict[str, str]] = None) -> str:
    result = encrypt_bytes(plaintext.encode("utf-8"), key_id=key_id, encryption_context=encryption_context)
    return result["ciphertext_blob"]


def decrypt_text(ciphertext_blob_b64: str, encryption_context: Optional[Dict[str, str]] = None) -> str:
    return decrypt_bytes(ciphertext_blob_b64, encryption_context=encryption_context).decode("utf-8")


def _safe_kms_call(method_name: str, *args: Any, **kwargs: Any) -> Any:
    client = create_kms_client()
    method = getattr(client, method_name)
    try:
        return method(*args, **kwargs)
    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError(f"KMS {method_name} failed: {exc}") from exc
