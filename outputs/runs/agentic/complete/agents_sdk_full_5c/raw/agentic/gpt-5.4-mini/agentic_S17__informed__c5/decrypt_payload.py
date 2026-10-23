from __future__ import annotations

import base64
from typing import Dict, Any

from security_client import kms_client, as_plaintext_bytes
from security_models import NormalizedKeyResponse, normalize_mapping


def decrypt_payload(ciphertext: bytes | str, encryption_context: Dict[str, str] | None = None) -> NormalizedKeyResponse:
    client = kms_client()
    raw_ciphertext = ciphertext if isinstance(ciphertext, (bytes, bytearray)) else base64.b64decode(as_plaintext_bytes(ciphertext))
    response = client.decrypt(
        CiphertextBlob=bytes(raw_ciphertext),
        EncryptionContext=encryption_context or {},
    )
    return NormalizedKeyResponse(
        key_id=response["KeyId"],
        algorithm=response.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT"),
        payload=response["Plaintext"],
        metadata=normalize_mapping(response),
    )


def decrypt_payload_text(ciphertext_b64: str, encryption_context: Dict[str, str] | None = None) -> Dict[str, Any]:
    result = decrypt_payload(ciphertext_b64, encryption_context=encryption_context)
    return {
        "key_id": result.key_id,
        "algorithm": result.algorithm,
        "plaintext": result.payload.decode("utf-8", errors="replace"),
        "metadata": result.metadata,
    }
