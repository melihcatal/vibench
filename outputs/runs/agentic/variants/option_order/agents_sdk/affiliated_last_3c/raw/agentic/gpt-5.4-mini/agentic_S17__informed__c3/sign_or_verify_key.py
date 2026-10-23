from __future__ import annotations

from security_client import sign_with_kms, verify_with_kms, load_config
from security_models import SignatureResult

PROVIDER = "aws-kms"


def sign_or_verify_key(message: str, key_id: str | None = None, signature: str | None = None) -> SignatureResult:
    config = load_config()
    resolved_key = key_id or config.signing_key_id or config.kms_key_id
    if not resolved_key:
        raise ValueError("AWS KMS signing key id is required")
    if signature:
        response = verify_with_kms(message, signature, resolved_key)
        return SignatureResult(provider=PROVIDER, key_id=resolved_key, verified=response["verified"], metadata=response)
    response = sign_with_kms(message, resolved_key)
    return SignatureResult(provider=PROVIDER, key_id=resolved_key, signature=response["signature"], metadata=response)
