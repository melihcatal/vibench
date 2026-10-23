from __future__ import annotations

from typing import Dict, Optional

from security_client import decode_b64, get_kms_client, kms_context
from security_models import CiphertextPayload, CryptoOperationResult


def decrypt_payload(
    ciphertext: str,
    encryption_context: Optional[Dict[str, str]] = None,
    key_id: Optional[str] = None,
) -> Dict[str, object]:
    payload = CiphertextPayload(
        ciphertext=ciphertext,
        key_id=key_id,
        encryption_context=kms_context(encryption_context),
    )
    kms_client = get_kms_client()
    response = kms_client.decrypt(
        CiphertextBlob=decode_b64(payload.ciphertext),
        KeyId=payload.key_id,
        EncryptionContext=payload.encryption_context,
    )
    result = CryptoOperationResult(
        provider="aws-kms",
        operation="decrypt",
        key_id=response.get("KeyId"),
        metadata={
            "plaintext": response["Plaintext"].decode("utf-8"),
            "encryption_algorithm": response.get("EncryptionAlgorithm"),
        },
    )
    return result.to_dict()
