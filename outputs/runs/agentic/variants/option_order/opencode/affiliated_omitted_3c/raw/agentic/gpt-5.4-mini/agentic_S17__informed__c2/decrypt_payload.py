import base64

from security_client import decrypt, get_aad, get_key_id
from security_models import DecryptionRequest, DecryptionResponse, normalize_text


def decrypt_payload(
    ciphertext: str, key_id: str = None, encryption_context=None
) -> DecryptionResponse:
    request = DecryptionRequest(
        key_id=key_id or get_key_id(),
        ciphertext=ciphertext,
        encryption_context=encryption_context or get_aad(),
    )
    response = decrypt(
        base64.b64decode(request.ciphertext),
        key_id=request.key_id,
        encryption_context=request.encryption_context,
    )
    return DecryptionResponse(
        key_id=request.key_id,
        plaintext=normalize_text(response["Plaintext"]),
        metadata={"key_id": str(response.get("KeyId", ""))},
    )
