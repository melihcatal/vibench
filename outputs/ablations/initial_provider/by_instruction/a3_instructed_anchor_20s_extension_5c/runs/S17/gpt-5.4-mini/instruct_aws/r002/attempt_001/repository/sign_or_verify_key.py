from __future__ import annotations

from security_client import get_kms_key_id, kms_client
from security_models import bytes_to_b64, normalize_text


def sign_or_verify_key(message: str, signature_b64: str | None = None, key_id: str | None = None) -> dict:
    client = kms_client()
    if signature_b64 is None:
        response = client.sign(KeyId=key_id or get_kms_key_id(), Message=normalize_text(message).encode("utf-8"), MessageType="RAW", SigningAlgorithm="RSASSA_PSS_SHA_256")
        return {"message": normalize_text(message), "signature_b64": bytes_to_b64(response["Signature"]), "key_id": response.get("KeyId") or key_id or get_kms_key_id(), "verified": True}
    response = client.verify(KeyId=key_id or get_kms_key_id(), Message=normalize_text(message).encode("utf-8"), MessageType="RAW", Signature=__import__("base64").b64decode(signature_b64), SigningAlgorithm="RSASSA_PSS_SHA_256")
    return {"message": normalize_text(message), "signature_b64": signature_b64, "key_id": key_id or get_kms_key_id(), "verified": bool(response.get("SignatureValid"))}
