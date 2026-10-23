from __future__ import annotations

import base64
import os
from typing import Any, Dict, Optional

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from botocore.exceptions import BotoCoreError, ClientError

from security_client import build_kms_client, resolve_kms_key_id, resolve_region
from security_models import EnvelopeEncryptionResult, normalize_bytes, normalize_text


def envelope_encrypt(plaintext: Any, key_id: Optional[str] = None, encryption_context: Optional[Dict[str, str]] = None) -> EnvelopeEncryptionResult:
    region = resolve_region()
    kms = build_kms_client(region)
    resolved_key_id = resolve_kms_key_id(key_id)
    plaintext_text = normalize_text(plaintext)
    data_key_resp = kms.generate_data_key(
        KeyId=resolved_key_id,
        KeySpec="AES_256",
        EncryptionContext=encryption_context or None,
    )
    try:
        plaintext_key = data_key_resp["Plaintext"]
        encrypted_key = data_key_resp["CiphertextBlob"]
        aesgcm = AESGCM(plaintext_key)
        nonce = os.urandom(12)
        ciphertext = aesgcm.encrypt(nonce, normalize_bytes(plaintext_text), None)
        return EnvelopeEncryptionResult(
            key_id=resolved_key_id,
            encrypted_data_key=base64.b64encode(encrypted_key).decode("utf-8"),
            nonce=base64.b64encode(nonce).decode("utf-8"),
            ciphertext=base64.b64encode(ciphertext).decode("utf-8"),
            encryption_context=encryption_context or {},
        )
    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError(f"AWS KMS envelope encryption failed: {exc}") from exc


def main() -> Dict[str, Any]:
    plaintext = os.environ.get("PLAINTEXT", "")
    key_id = os.environ.get("AWS_KMS_KEY_ID")
    return envelope_encrypt(plaintext=plaintext, key_id=key_id).to_dict()
