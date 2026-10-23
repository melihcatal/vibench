from __future__ import annotations

from security_client import decrypt_with_kms, load_configuration
from security_models import DecryptionRequest

PROVIDER = "AWS Key Management Service"


def decrypt_payload(ciphertext: str, key_id: str | None = None, aad: str | None = None):
    cfg = load_configuration()
    request = DecryptionRequest(key_id=key_id or cfg["kms_key_id"], ciphertext=ciphertext, aad=aad)
    return decrypt_with_kms(request, region_name=cfg["aws_region"])
