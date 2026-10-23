from __future__ import annotations

from security_client import sign_with_kms, verify_with_kms
from security_models import SignatureResult


def sign_or_verify_key(message: bytes, signature: bytes | None = None, key_id: str | None = None) -> SignatureResult:
    if signature is None:
        signed = sign_with_kms(message, key_id=key_id)
        return SignatureResult(signature=signed, key_id=key_id or "", verified=None)
    verified = verify_with_kms(message, signature, key_id=key_id)
    return SignatureResult(signature=signature, key_id=key_id or "", verified=verified)
