import base64

from security_client import get_kms_client, normalize_key_id
from security_models import normalize_context


def decrypt_payload(ciphertext: str, key_id: str | None = None, context=None) -> str:
    kms = get_kms_client()
    params = {"CiphertextBlob": base64.b64decode(ciphertext.encode("utf-8"))}
    if key_id:
        params["KeyId"] = normalize_key_id(key_id)
    ctx = normalize_context(context)
    if ctx:
        params["EncryptionContext"] = ctx
    result = kms.decrypt(**params)
    return result["Plaintext"].decode("utf-8")
