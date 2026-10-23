import base64

from security_client import encrypt, get_aad, get_key_id
from security_models import PayloadRequest, CiphertextResponse, normalize_bytes


def encrypt_payload(
    plaintext: str, key_id: str = None, encryption_context=None
) -> CiphertextResponse:
    request = PayloadRequest(
        key_id=key_id or get_key_id(),
        plaintext=plaintext,
        encryption_context=encryption_context or get_aad(),
    )
    response = encrypt(
        normalize_bytes(request.plaintext),
        key_id=request.key_id,
        encryption_context=request.encryption_context,
    )
    return CiphertextResponse(
        key_id=request.key_id,
        ciphertext=base64.b64encode(response["CiphertextBlob"]).decode("utf-8"),
        metadata={"arn": str(response.get("KeyId", ""))},
    )
