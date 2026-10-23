from __future__ import annotations

from typing import Any, Dict, Optional

from security_client import get_kms_client
from security_models import PlaintextResponse, b64decode_str, normalize_metadata


def decrypt_payload(
    ciphertext_b64: str,
    encryption_context: Optional[Dict[str, str]] = None,
    metadata: Optional[Dict[str, Any]] = None,
    region_name: Optional[str] = None,
) -> Dict[str, Any]:
    kms_client = get_kms_client(region_name)
    response = kms_client.decrypt(
        CiphertextBlob=b64decode_str(ciphertext_b64),
        EncryptionContext=encryption_context or None,
    )
    result = PlaintextResponse(
        key_id=response["KeyId"],
        provider="aws-kms",
        plaintext=response["Plaintext"].decode("utf-8"),
        encryption_context=encryption_context or {},
        metadata=normalize_metadata(metadata),
    )
    return result.to_dict()
