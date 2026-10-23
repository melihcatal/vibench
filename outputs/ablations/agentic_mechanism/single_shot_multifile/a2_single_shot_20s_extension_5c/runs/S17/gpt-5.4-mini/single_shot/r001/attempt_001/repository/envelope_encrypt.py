from __future__ import annotations

import base64
import os
from typing import Any, Dict

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from google.cloud import kms_v1

from security_client import get_kms_key_name, get_kms_key_ring, get_kms_location, get_project_id
from security_models import EnvelopeEncryptionResult, normalize_plaintext_payload


def envelope_encrypt(payload: Any, key_name: str | None = None) -> Dict[str, Any]:
    project_id = get_project_id()
    location = get_kms_location()
    key_ring = get_kms_key_ring()
    resolved_key_name = key_name or get_kms_key_name(project_id=project_id, location=location, key_ring=key_ring)
    kms_client = kms_v1.KeyManagementServiceClient()
    dek = AESGCM.generate_key(bit_length=256)
    wrapped_dek = kms_client.encrypt(request={"name": resolved_key_name, "plaintext": dek}).ciphertext
    aesgcm = AESGCM(dek)
    nonce = os.urandom(12)
    plaintext = normalize_plaintext_payload(payload)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    result = EnvelopeEncryptionResult(
        key_name=resolved_key_name,
        encrypted_key=base64.b64encode(wrapped_dek).decode("utf-8"),
        nonce=base64.b64encode(nonce).decode("utf-8"),
        ciphertext=base64.b64encode(ciphertext).decode("utf-8"),
        metadata={"provider": "google-cloud-kms", "algorithm": "AES-256-GCM"},
    )
    return result.to_dict()
