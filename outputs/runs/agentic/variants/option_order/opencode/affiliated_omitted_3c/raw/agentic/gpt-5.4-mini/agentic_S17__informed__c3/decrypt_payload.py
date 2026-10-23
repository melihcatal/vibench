import base64

from security_client import get_config, get_kms_client
from security_models import CryptoResult, normalize_text


def decrypt_payload(
    ciphertext: str, key_id: str | None = None, context: dict | None = None
) -> CryptoResult:
    cfg = get_config()
    client = get_kms_client()
    blob = base64.b64decode(normalize_text(ciphertext).encode("ascii"))
    kwargs = {"CiphertextBlob": blob}
    if context:
        kwargs["EncryptionContext"] = context
    resp = client.decrypt(**kwargs)
    plaintext = resp["Plaintext"].decode("utf-8")
    return CryptoResult(
        success=True,
        payload=plaintext,
        key_id=key_id or cfg["default_key_id"],
        provider=cfg["provider"],
    )
