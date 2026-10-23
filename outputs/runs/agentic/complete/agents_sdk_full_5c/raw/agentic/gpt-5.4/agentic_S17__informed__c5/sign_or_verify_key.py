from __future__ import annotations

from typing import Literal

from security_client import kms_client
from security_models import b64encode_str
import base64


MessageType = Literal["RAW", "DIGEST"]


def sign_with_key(key_id: str, message: bytes, signing_algorithm: str = "RSASSA_PSS_SHA_256", message_type: MessageType = "RAW") -> dict:
    client = kms_client()
    response = client.sign(
        KeyId=key_id,
        Message=message,
        MessageType=message_type,
        SigningAlgorithm=signing_algorithm,
    )
    return {
        "provider": "aws-kms",
        "operation": "sign",
        "key_id": response["KeyId"],
        "signing_algorithm": response["SigningAlgorithm"],
        "signature_b64": b64encode_str(response["Signature"]),
        "aws_region": client.meta.region_name,
    }


def verify_with_key(key_id: str, message: bytes, signature_b64: str, signing_algorithm: str = "RSASSA_PSS_SHA_256", message_type: MessageType = "RAW") -> dict:
    client = kms_client()
    response = client.verify(
        KeyId=key_id,
        Message=message,
        MessageType=message_type,
        Signature=base64.b64decode(signature_b64),
        SigningAlgorithm=signing_algorithm,
    )
    return {
        "provider": "aws-kms",
        "operation": "verify",
        "key_id": response["KeyId"],
        "signing_algorithm": response["SigningAlgorithm"],
        "signature_valid": response["SignatureValid"],
        "aws_region": client.meta.region_name,
    }
