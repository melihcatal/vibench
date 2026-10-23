from __future__ import annotations

import os
from typing import Any, Dict, Optional

from google.cloud import kms_v1

from security_client import build_kms_client, resolve_crypto_key_name
from security_models import SignatureRequest, SignatureResponse, VerificationRequest, VerificationResponse, from_json_safe_bytes, to_json_safe_bytes


def sign_or_verify_key(message: str, signature: Optional[str] = None, key_name: Optional[str] = None) -> Dict[str, Any]:
    client = build_kms_client()
    crypto_key = resolve_crypto_key_name(key_name or os.getenv("GOOGLE_CLOUD_KMS_CRYPTO_KEY"))
    if signature is None:
        request = SignatureRequest(message=message, key_name=crypto_key)
        digest = kms_v1.Digest()
        digest.sha256 = __import__("hashlib").sha256(request.message.encode("utf-8")).digest()
        signed = client.asymmetric_sign(request={"name": request.key_name, "digest": {"sha256": digest.sha256}})
        result = SignatureResponse(key_name=crypto_key, signature=signed.signature)
        return {"mode": "sign", "key_name": result.key_name, "signature": to_json_safe_bytes(result.signature)}
    request = VerificationRequest(message=message, signature=from_json_safe_bytes(signature), key_name=crypto_key)
    digest = __import__("hashlib").sha256(request.message.encode("utf-8")).digest()
    verified = client.asymmetric_verify(request={"name": request.key_name, "digest": {"sha256": digest}, "signature": request.signature})
    result = VerificationResponse(key_name=crypto_key, verified=bool(verified.name))
    return {"mode": "verify", "key_name": result.key_name, "verified": result.verified}
