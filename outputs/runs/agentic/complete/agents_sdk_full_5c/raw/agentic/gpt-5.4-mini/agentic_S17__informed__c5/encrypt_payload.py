from __future__ import annotations

import base64
from typing import Dict, Any

from security_client import kms_client, kms_key_id, as_plaintext_bytes
from security_models import NormalizedKeyResponse, normalize_mapping


def encrypt_payload(plaintext: str, encryption_context: Dict[str, str] | None = None) -> NormalizedKeyResponse:
    client = kms_client()
    response = client.encrypt(
        KeyId=kms_key_id(),
        Plaintext=as_plaintext_bytes(plaintext),
        EncryptionContext=encryption_context or {},
    )
    return NormalizedKeyResponse(
        key_id=response["KeyId"],
        algorithm=response.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT"),
        payload=response["CiphertextBlob"],
        metadata=normalize_mapping(response),
    )


def encrypt_payload_base64(plaintext: str, encryption_context: Dict[str, str] | None = None) -> Dict[str, Any]:
    result = encrypt_payload(plaintext, encryption_context=encryption_context)
    return {
        "key_id": result.key_id,
        "algorithm": result.algorithm,
        "ciphertext_b64": base64.b64encode(result.payload).decode("ascii"),
        "metadata": result.metadata,
    }
