import os
from typing import Any, Dict, Optional

from botocore.exceptions import BotoCoreError, ClientError
import boto3

from security_models import normalize_mapping, normalize_text


def load_security_config() -> Dict[str, Any]:
    return {
        "aws_region": os.getenv("AWS_REGION", "us-east-1"),
        "kms_key_id": os.getenv("AWS_KMS_KEY_ID", "alias/default"),
        "signature_key_id": os.getenv(
            "AWS_KMS_SIGNING_KEY_ID", os.getenv("AWS_KMS_KEY_ID", "alias/default")
        ),
    }


def get_kms_client(region_name: Optional[str] = None):
    cfg = load_security_config()
    return boto3.client("kms", region_name=region_name or cfg["aws_region"])


def encrypt_bytes(
    plaintext: str, key_id: Optional[str] = None, aad: Optional[str] = None
) -> Dict[str, Any]:
    client = get_kms_client()
    params: Dict[str, Any] = {
        "KeyId": key_id or load_security_config()["kms_key_id"],
        "Plaintext": normalize_text(plaintext).encode("utf-8"),
    }
    if aad is not None:
        params["EncryptionContext"] = {"aad": normalize_text(aad)}
    response = client.encrypt(**params)
    return normalize_mapping(response)


def decrypt_bytes(ciphertext_blob: bytes, aad: Optional[str] = None) -> Dict[str, Any]:
    client = get_kms_client()
    params: Dict[str, Any] = {"CiphertextBlob": ciphertext_blob}
    if aad is not None:
        params["EncryptionContext"] = {"aad": normalize_text(aad)}
    response = client.decrypt(**params)
    return normalize_mapping(response)


def generate_data_key(key_id: Optional[str] = None) -> Dict[str, Any]:
    client = get_kms_client()
    response = client.generate_data_key(
        KeyId=key_id or load_security_config()["kms_key_id"], KeySpec="AES_256"
    )
    return normalize_mapping(response)


def sign_message(message: bytes, key_id: Optional[str] = None) -> Dict[str, Any]:
    client = get_kms_client()
    response = client.sign(
        KeyId=key_id or load_security_config()["signature_key_id"],
        Message=message,
        MessageType="RAW",
        SigningAlgorithm="RSASSA_PSS_SHA_256",
    )
    return normalize_mapping(response)


def verify_message(
    message: bytes, signature: bytes, key_id: Optional[str] = None
) -> Dict[str, Any]:
    client = get_kms_client()
    response = client.verify(
        KeyId=key_id or load_security_config()["signature_key_id"],
        Message=message,
        Signature=signature,
        MessageType="RAW",
        SigningAlgorithm="RSASSA_PSS_SHA_256",
    )
    return normalize_mapping(response)
