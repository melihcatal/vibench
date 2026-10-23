from security_client import encryption_context, kms_client, kms_key_id
from security_models import KeyRequest, KeyResponse, b64e, normalize_context


def encrypt_payload(plaintext: bytes, key_id: str = "") -> KeyResponse:
    client = kms_client()
    resolved_key_id = key_id or kms_key_id()
    request = KeyRequest(key_id=resolved_key_id, plaintext=plaintext, encryption_context=normalize_context(encryption_context()))
    params = {"KeyId": request.key_id, "Plaintext": request.plaintext}
    if request.encryption_context:
        params["EncryptionContext"] = request.encryption_context
    response = client.encrypt(**params)
    return KeyResponse(key_id=response["KeyId"], ciphertext=response["CiphertextBlob"], encryption_context=request.encryption_context)


def encrypt_payload_text(text: str, key_id: str = "") -> str:
    return b64e(encrypt_payload(text.encode(), key_id).ciphertext)
