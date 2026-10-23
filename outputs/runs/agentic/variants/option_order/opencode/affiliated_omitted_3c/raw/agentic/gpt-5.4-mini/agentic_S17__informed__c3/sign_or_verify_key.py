import base64

from security_client import get_config, get_kms_client
from security_models import CryptoResult, normalize_text


def sign_or_verify_key(
    message: str, key_id: str | None = None, signature: str | None = None
):
    cfg = get_config()
    client = get_kms_client()
    resolved_key_id = key_id or cfg["default_key_id"]
    payload = normalize_text(message).encode("utf-8")
    if signature is None:
        resp = client.sign(
            KeyId=resolved_key_id,
            Message=payload,
            MessageType="RAW",
            SigningAlgorithm=cfg["signing_algorithm"],
        )
        return CryptoResult(
            success=True,
            payload=base64.b64encode(resp["Signature"]).decode("ascii"),
            key_id=resolved_key_id,
            provider=cfg["provider"],
        )
    ok = client.verify(
        KeyId=resolved_key_id,
        Message=payload,
        MessageType="RAW",
        Signature=base64.b64decode(normalize_text(signature).encode("ascii")),
        SigningAlgorithm=cfg["signing_algorithm"],
    )
    return CryptoResult(
        success=bool(ok.get("SignatureValid")),
        payload="verified" if ok.get("SignatureValid") else "failed",
        key_id=resolved_key_id,
        provider=cfg["provider"],
    )
