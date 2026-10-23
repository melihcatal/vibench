from __future__ import annotations

import base64
import json
import os
from typing import Any, Dict

from security_client import kms_client, kms_key_id, as_plaintext_bytes
from security_models import NormalizedKeyResponse, normalize_mapping

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except Exception:  # pragma: no cover
    AESGCM = None


def envelope_encrypt(plaintext: str, encryption_context: Dict[str, str] | None = None) -> Dict[str, Any]:
    if AESGCM is None:
        raise RuntimeError("cryptography package is required for envelope encryption")

    client = kms_client()
    data_key = client.generate_data_key(KeyId=kms_key_id(), KeySpec="AES_256", EncryptionContext=encryption_context or {})
    plaintext_key = data_key["Plaintext"]
    encrypted_key = data_key["CiphertextBlob"]

    aesgcm = AESGCM(plaintext_key)
    nonce = os.urandom(12)
    aad = json.dumps(encryption_context or {}, sort_keys=True).encode("utf-8")
    ciphertext = aesgcm.encrypt(nonce, as_plaintext_bytes(plaintext), aad)

    response = NormalizedKeyResponse(
        key_id=data_key["KeyId"],
        algorithm="AES_256_GCM_ENVELOPE",
        payload=ciphertext,
        nonce=nonce,
        metadata=normalize_mapping(data_key),
    )
    return {
        "key_id": response.key_id,
        "algorithm": response.algorithm,
        "encrypted_data_key_b64": base64.b64encode(encrypted_key).decode("ascii"),
        "nonce_b64": base64.b64encode(response.nonce).decode("ascii"),
        "ciphertext_b64": base64.b64encode(response.payload).decode("ascii"),
        "metadata": response.metadata,
    }
