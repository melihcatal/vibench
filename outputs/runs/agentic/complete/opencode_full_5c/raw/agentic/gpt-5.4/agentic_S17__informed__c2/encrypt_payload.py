from __future__ import annotations

from typing import Dict, Optional

from security_client import encode_b64, get_kms_client, get_kms_key_id, kms_context
from security_models import CryptoOperationResult, PlaintextPayload


def encrypt_payload(
    plaintext: str,
    key_id: Optional[str] = None,
    encryption_context: Optional[Dict[str, str]] = None,
) -> Dict[str, object]:
    payload = PlaintextPayload(
        plaintext=plaintext,
        key_id=key_id,
        encryption_context=kms_context(encryption_context),
    )
    kms_client = get_kms_client()
    response = kms_client.encrypt(
        KeyId=get_kms_key_id(payload.key_id),
        Plaintext=payload.to_bytes(),
        EncryptionContext=payload.encryption_context,
    )
    result = CryptoOperationResult(
        provider="aws-kms",
        operation="encrypt",
        key_id=response.get("KeyId"),
        metadata={
            "ciphertext": encode_b64(response["CiphertextBlob"]),
            "encryption_algorithm": response.get("EncryptionAlgorithm"),
        },
    )
    return result.to_dict()
