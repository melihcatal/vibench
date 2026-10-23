from __future__ import annotations

from security_client import encrypt_with_kms, load_configuration, normalize_text_payload
from security_models import EncryptionRequest

PROVIDER = "AWS Key Management Service"


def encrypt_payload(plaintext: str, key_id: str | None = None, aad: str | None = None):
    cfg = load_configuration()
    normalized = normalize_text_payload(plaintext)
    request = EncryptionRequest(key_id=key_id or cfg["kms_key_id"], plaintext=normalized.text, aad=aad)
    return encrypt_with_kms(request, region_name=cfg["aws_region"])
