from __future__ import annotations

from typing import Dict, Any

from security_client import kms_client
from security_models import DecryptRequest, DecryptResponse, b64decode_text, bytes_to_text



def decrypt_payload(request: DecryptRequest) -> DecryptResponse:
    client = kms_client()
    response = client.decrypt(
        CiphertextBlob=b64decode_text(request.ciphertext_b64),
        EncryptionContext=request.encryption_context or None,
    )
    return DecryptResponse(
        key_id=response["KeyId"],
        plaintext=bytes_to_text(response["Plaintext"]),
    )



def decrypt_payload_dict(ciphertext_b64: str, encryption_context: Dict[str, str] | None = None) -> Dict[str, Any]:
    result = decrypt_payload(DecryptRequest(ciphertext_b64=ciphertext_b64, encryption_context=encryption_context or {}))
    return {
        "provider": result.provider,
        "key_id": result.key_id,
        "plaintext": result.plaintext,
    }
