from __future__ import annotations

from typing import Any, Dict, Optional

from security_client import get_kms_client
from security_models import (
    CiphertextResponse,
    PayloadRequest,
    b64encode_str,
    normalize_metadata,
)


def encrypt_payload(
    key_id: str,
    plaintext: str,
    encryption_context: Optional[Dict[str, str]] = None,
    metadata: Optional[Dict[str, Any]] = None,
    region_name: Optional[str] = None,
) -> Dict[str, Any]:
    request = PayloadRequest(
        key_id=key_id,
        plaintext=plaintext,
        encryption_context=encryption_context or {},
        metadata=normalize_metadata(metadata),
    )
    kms_client = get_kms_client(region_name)
    response = kms_client.encrypt(
        KeyId=request.key_id,
        Plaintext=request.plaintext_bytes(),
        EncryptionContext=request.encryption_context or None,
    )
    result = CiphertextResponse(
        key_id=response["KeyId"],
        provider="aws-kms",
        ciphertext_b64=b64encode_str(response["CiphertextBlob"]),
        algorithm=response.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT"),
        encryption_context=request.encryption_context,
        metadata=request.metadata,
    )
    return result.to_dict()
