from __future__ import annotations

import os
from typing import Any, Dict

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from security_client import (
    kms_client,
    normalize_encryption_context,
    provider_name,
    resolve_key_id,
)
from security_models import (
    EnvelopeEncryptRequest,
    EnvelopeEncryptResponse,
    sha256_text,
    to_b64,
    utc_now_iso,
)


def envelope_encrypt(payload: Dict[str, Any]) -> Dict[str, Any]:
    request = EnvelopeEncryptRequest(
        key_id=resolve_key_id(payload.get("key_id")),
        plaintext=str(payload["plaintext"]),
        encryption_context=normalize_encryption_context(
            payload.get("encryption_context")
        ),
    )
    generated = kms_client().generate_data_key(
        KeyId=request.key_id,
        KeySpec="AES_256",
        EncryptionContext=request.encryption_context,
    )
    iv = os.urandom(12)
    aesgcm = AESGCM(generated["Plaintext"])
    encrypted = aesgcm.encrypt(iv, request.plaintext.encode("utf-8"), None)
    ciphertext = encrypted[:-16]
    tag = encrypted[-16:]
    result = EnvelopeEncryptResponse(
        provider=provider_name(),
        key_id=generated["KeyId"],
        wrapped_data_key_b64=to_b64(generated["CiphertextBlob"]),
        ciphertext_b64=to_b64(ciphertext),
        iv_b64=to_b64(iv),
        tag_b64=to_b64(tag),
        encryption_context=request.encryption_context,
        plaintext_sha256=sha256_text(request.plaintext),
        created_at=utc_now_iso(),
    )
    return result.to_dict()
