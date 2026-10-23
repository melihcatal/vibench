from __future__ import annotations

from typing import Dict, Any

from security_client import kms_client
from security_models import EncryptRequest, EncryptResponse, b64encode_bytes, text_to_bytes



def encrypt_payload(request: EncryptRequest) -> EncryptResponse:
    client = kms_client()
    response = client.encrypt(
        KeyId=request.key_id,
        Plaintext=text_to_bytes(request.plaintext),
        EncryptionContext=request.encryption_context or None,
    )
    return EncryptResponse(
        key_id=response["KeyId"],
        ciphertext_b64=b64encode_bytes(response["CiphertextBlob"]),
        algorithm=response.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT"),
    )



def encrypt_payload_dict(key_id: str, plaintext: str, encryption_context: Dict[str, str] | None = None) -> Dict[str, Any]:
    result = encrypt_payload(EncryptRequest(key_id=key_id, plaintext=plaintext, encryption_context=encryption_context or {}))
    return {
        "provider": result.provider,
        "key_id": result.key_id,
        "ciphertext_b64": result.ciphertext_b64,
        "algorithm": result.algorithm,
    }
