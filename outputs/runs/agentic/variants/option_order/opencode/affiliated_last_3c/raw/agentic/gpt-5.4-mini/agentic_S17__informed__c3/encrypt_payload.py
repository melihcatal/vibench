import base64

from security_client import encrypt_bytes
from security_models import PayloadRequest, CiphertextResponse, normalize_text


def encrypt_payload(plaintext: str, key_id: str, aad: str = None) -> CiphertextResponse:
    request = PayloadRequest(
        plaintext=normalize_text(plaintext),
        key_id=normalize_text(key_id),
        aad=normalize_text(aad) if aad is not None else None,
    )
    result = encrypt_bytes(request.plaintext, request.key_id, request.aad)
    return CiphertextResponse(
        ciphertext=base64.b64encode(result["CiphertextBlob"]).decode("ascii"),
        key_id=request.key_id,
        metadata={"provider": "aws-kms", "key_id": request.key_id},
    )
