from __future__ import annotations

from typing import Any, Dict

from security_client import (
    kms_client,
    normalize_encryption_context,
    provider_name,
    resolve_key_id,
)
from security_models import (
    EncryptPayloadRequest,
    EncryptPayloadResponse,
    sha256_text,
    to_b64,
    utc_now_iso,
)


def encrypt_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    request = EncryptPayloadRequest(
        key_id=resolve_key_id(payload.get("key_id")),
        plaintext=str(payload["plaintext"]),
        encryption_context=normalize_encryption_context(
            payload.get("encryption_context")
        ),
    )
    response = kms_client().encrypt(
        KeyId=request.key_id,
        Plaintext=request.plaintext.encode("utf-8"),
        EncryptionContext=request.encryption_context,
    )
    result = EncryptPayloadResponse(
        provider=provider_name(),
        key_id=response["KeyId"],
        ciphertext_b64=to_b64(response["CiphertextBlob"]),
        encryption_algorithm=response.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT"),
        encryption_context=request.encryption_context,
        plaintext_sha256=sha256_text(request.plaintext),
        created_at=utc_now_iso(),
    )
    return result.to_dict()
