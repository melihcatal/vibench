from __future__ import annotations

import base64
from typing import Any, Dict

from security_client import kms_client, signing_key_id, as_plaintext_bytes
from security_models import NormalizedKeyResponse, normalize_mapping


def sign_payload(message: str) -> NormalizedKeyResponse:
    client = kms_client()
    response = client.sign(
        KeyId=signing_key_id(),
        Message=as_plaintext_bytes(message),
        SigningAlgorithm="RSASSA_PSS_SHA_256",
        MessageType="RAW",
    )
    return NormalizedKeyResponse(
        key_id=response["KeyId"],
        algorithm=response.get("SigningAlgorithm", "RSASSA_PSS_SHA_256"),
        signature=response["Signature"],
        metadata=normalize_mapping(response),
    )


def verify_signature(message: str, signature_b64: str, key_id: str | None = None) -> Dict[str, Any]:
    client = kms_client()
    response = client.verify(
        KeyId=key_id or signing_key_id(),
        Message=as_plaintext_bytes(message),
        Signature=base64.b64decode(signature_b64),
        SigningAlgorithm="RSASSA_PSS_SHA_256",
        MessageType="RAW",
    )
    return {
        "key_id": response["KeyId"],
        "signature_valid": response.get("SignatureValid", False),
        "algorithm": response.get("SigningAlgorithm", "RSASSA_PSS_SHA_256"),
        "metadata": normalize_mapping(response),
    }
