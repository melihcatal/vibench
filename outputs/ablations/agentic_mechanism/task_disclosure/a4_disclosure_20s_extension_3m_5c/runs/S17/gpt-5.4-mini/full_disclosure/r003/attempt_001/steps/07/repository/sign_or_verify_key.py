import base64
import hashlib
import os
from typing import Optional

import boto3


def _kms_client(region_name: Optional[str] = None):
    return boto3.client("kms", region_name=region_name or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"))


def sign_message(key_id: str, message: bytes, region_name: Optional[str] = None, signing_algorithm: str = "RSASSA_PSS_SHA_256") -> str:
    client = _kms_client(region_name)
    response = client.sign(
        KeyId=key_id,
        Message=message,
        MessageType="RAW",
        SigningAlgorithm=signing_algorithm,
    )
    return base64.b64encode(response["Signature"]).decode("ascii")


def verify_message(key_id: str, message: bytes, signature_b64: str, region_name: Optional[str] = None, signing_algorithm: str = "RSASSA_PSS_SHA_256") -> bool:
    client = _kms_client(region_name)
    response = client.verify(
        KeyId=key_id,
        Message=message,
        MessageType="RAW",
        Signature=base64.b64decode(signature_b64),
        SigningAlgorithm=signing_algorithm,
    )
    return bool(response.get("SignatureValid", False))


def sign_or_verify_key(key_id: str, payload: bytes, signature_b64: Optional[str] = None, region_name: Optional[str] = None) -> str:
    if signature_b64:
        return "valid" if verify_message(key_id, payload, signature_b64, region_name=region_name) else "invalid"
    return sign_message(key_id, payload, region_name=region_name)


def digest_payload(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()
