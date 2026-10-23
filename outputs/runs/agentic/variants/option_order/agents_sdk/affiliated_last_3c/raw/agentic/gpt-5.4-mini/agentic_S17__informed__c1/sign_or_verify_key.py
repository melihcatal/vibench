from __future__ import annotations

import base64

from security_client import sign_with_kms, verify_with_kms, load_security_config
from security_models import SignRequest, VerifyRequest


def sign_or_verify_key(message: str, key_id: str | None = None, signature_b64: str | None = None) -> dict:
    config = load_security_config()
    resolved_key_id = key_id or config.signing_key_id or config.kms_key_id
    if not resolved_key_id:
        raise ValueError("Signing key id is required")
    message_bytes = message.encode("utf-8")
    if signature_b64:
        verify_request = VerifyRequest(key_id=resolved_key_id, message=message_bytes, signature=base64.b64decode(signature_b64))
        result = verify_with_kms(verify_request)
        return {"provider": result.provider, "key_id": result.key_id, "verified": result.ok, "details": result.payload, "error": result.error}
    sign_request = SignRequest(key_id=resolved_key_id, message=message_bytes)
    result = sign_with_kms(sign_request)
    return {"provider": result.provider, "key_id": result.key_id, "signature_b64": result.payload["signature"], "error": result.error}
