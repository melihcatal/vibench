from __future__ import annotations

from typing import Any, Dict, Optional
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from security_client import get_kms_client
from security_models import (
    EnvelopeEncryptionResponse,
    normalize_metadata,
    to_bytes,
    b64encode_str,
)


def envelope_encrypt(
    key_id: str,
    plaintext: str,
    encryption_context: Optional[Dict[str, str]] = None,
    metadata: Optional[Dict[str, Any]] = None,
    region_name: Optional[str] = None,
) -> Dict[str, Any]:
    kms_client = get_kms_client(region_name)
    context = encryption_context or {}
    data_key_response = kms_client.generate_data_key(
        KeyId=key_id,
        KeySpec="AES_256",
        EncryptionContext=context or None,
    )
    data_key_plaintext = data_key_response["Plaintext"]
    nonce = os.urandom(12)
    aad = (
        "|".join(f"{k}={v}" for k, v in sorted(context.items())).encode("utf-8")
        if context
        else None
    )
    ciphertext = AESGCM(data_key_plaintext).encrypt(nonce, to_bytes(plaintext), aad)
    result = EnvelopeEncryptionResponse(
        provider="aws-kms",
        kms_key_id=data_key_response["KeyId"],
        encrypted_data_key_b64=b64encode_str(data_key_response["CiphertextBlob"]),
        ciphertext_b64=b64encode_str(ciphertext),
        nonce_b64=b64encode_str(nonce),
        algorithm="AES-256-GCM",
        wrapping_algorithm="AWS KMS GenerateDataKey AES_256",
        encryption_context=context,
        metadata=normalize_metadata(metadata),
    )
    return result.to_dict()
