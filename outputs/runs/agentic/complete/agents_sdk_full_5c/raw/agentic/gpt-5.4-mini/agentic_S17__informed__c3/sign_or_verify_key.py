from __future__ import annotations

from security_client import load_configuration, sign_message, verify_signature
from security_models import SignOrVerifyRequest

PROVIDER = "AWS Key Management Service"


def sign_or_verify_key(message: str, key_id: str | None = None, signature: str | None = None):
    cfg = load_configuration()
    request = SignOrVerifyRequest(key_id=key_id or cfg["signing_key_id"], message=message, signature=signature)
    if signature:
        return verify_signature(request, region_name=cfg["aws_region"])
    return sign_message(request, region_name=cfg["aws_region"])
