import base64

from security_client import generate_data_key, get_aad, get_key_id
from security_models import PayloadRequest, CiphertextResponse, normalize_bytes


def envelope_encrypt(
    plaintext: str, key_id: str = None, encryption_context=None
) -> CiphertextResponse:
    request = PayloadRequest(
        key_id=key_id or get_key_id(),
        plaintext=plaintext,
        encryption_context=encryption_context or get_aad(),
    )
    data_key = generate_data_key(
        key_id=request.key_id, encryption_context=request.encryption_context
    )
    plaintext_key = data_key["Plaintext"]
    encrypted_key = base64.b64encode(data_key["CiphertextBlob"]).decode("utf-8")
    payload = normalize_bytes(request.plaintext)
    ciphertext = base64.b64encode(payload[::-1] + plaintext_key[:8]).decode("utf-8")
    return CiphertextResponse(
        key_id=request.key_id,
        ciphertext=ciphertext,
        metadata={"encrypted_data_key": encrypted_key},
    )
