from __future__ import annotations

import base64
import os
from typing import Any, Dict, Optional

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from google.cloud import kms_v1

from security_client import build_kms_client, resolve_crypto_key_name
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse, normalize_plaintext_bytes, to_json_safe_bytes


def envelope_encrypt(plaintext: str, key_name: Optional[str] = None, aad: Optional[bytes] = None) -> Dict[str, Any]:
    client = build_kms_client()
    crypto_key = resolve_crypto_key_name(key_name or os.getenv("GOOGLE_CLOUD_KMS_CRYPTO_KEY"))
    dek = AESGCM.generate_key(bit_length=256)
    encrypted_dek = client.encrypt(request={"name": crypto_key, "plaintext": dek}).ciphertext
    aesgcm = AESGCM(dek)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, normalize_plaintext_bytes(plaintext), aad)
    result = EnvelopeEncryptionResponse(
        key_name=crypto_key,
        encrypted_dek=encrypted_dek,
        nonce=nonce,
        ciphertext=ciphertext,
        aad=aad,
    )
    return {
        "key_name": result.key_name,
        "encrypted_dek": to_json_safe_bytes(result.encrypted_dek),
        "nonce": to_json_safe_bytes(result.nonce),
        "ciphertext": to_json_safe_bytes(result.ciphertext),
        "aad": to_json_safe_bytes(result.aad),
    }
