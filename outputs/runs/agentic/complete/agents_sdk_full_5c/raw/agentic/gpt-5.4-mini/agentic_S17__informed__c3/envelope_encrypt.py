from __future__ import annotations

import base64
import os
from typing import Any, Dict

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from security_client import generate_data_key, load_configuration, normalize_text_payload
from security_models import EnvelopeEncryptionRequest

PROVIDER = "AWS Key Management Service"


def envelope_encrypt(plaintext: str, key_id: str | None = None, aad: str | None = None) -> Dict[str, Any]:
    cfg = load_configuration()
    normalized = normalize_text_payload(plaintext)
    req = EnvelopeEncryptionRequest(key_id=key_id or cfg["kms_key_id"], plaintext=normalized.text, aad=aad)
    data_key = generate_data_key(req, region_name=cfg["aws_region"])
    key_bytes = base64.b64decode(data_key["plaintext_data_key"])
    aesgcm = AESGCM(key_bytes)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, normalized.text.encode("utf-8"), aad.encode("utf-8") if aad else None)
    return {
        "provider": PROVIDER,
        "key_id": req.key_id,
        "encrypted_data_key": data_key["encrypted_data_key"],
        "nonce": base64.b64encode(nonce).decode("ascii"),
        "ciphertext": base64.b64encode(ciphertext).decode("ascii"),
    }
