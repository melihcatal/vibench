from security_client import encryption_context, kms_client, kms_key_id
from security_models import KeyRequest, b64d, normalize_context


def decrypt_payload(ciphertext_b64: str, key_id: str = "") -> bytes:
    client = kms_client()
    resolved_key_id = key_id or kms_key_id()
    request = KeyRequest(key_id=resolved_key_id, plaintext=b"", encryption_context=normalize_context(encryption_context()))
    params = {"CiphertextBlob": b64d(ciphertext_b64)}
    if request.encryption_context:
        params["EncryptionContext"] = request.encryption_context
    response = client.decrypt(**params)
    return response["Plaintext"]
