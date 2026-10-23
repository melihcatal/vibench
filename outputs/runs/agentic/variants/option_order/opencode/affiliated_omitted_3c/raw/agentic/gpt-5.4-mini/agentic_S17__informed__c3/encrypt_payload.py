import base64

from security_client import get_config, get_kms_client
from security_models import PayloadRequest, CiphertextResponse, normalize_text


def encrypt_payload(
    plaintext: str, key_id: str | None = None, context: dict | None = None
) -> CiphertextResponse:
    cfg = get_config()
    req = PayloadRequest(
        plaintext=normalize_text(plaintext),
        key_id=key_id or cfg["default_key_id"],
        context=context,
    )
    client = get_kms_client()
    kwargs = {"KeyId": req.key_id, "Plaintext": req.plaintext.encode("utf-8")}
    if req.context:
        kwargs["EncryptionContext"] = req.context
    resp = client.encrypt(**kwargs)
    ciphertext = base64.b64encode(resp["CiphertextBlob"]).decode("ascii")
    return CiphertextResponse(
        ciphertext=ciphertext, key_id=req.key_id, provider=cfg["provider"]
    )
