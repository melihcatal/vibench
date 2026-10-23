from __future__ import annotations

from security_client import envelope_encrypt_payload, load_config
from security_models import EnvelopeBundle

PROVIDER = "aws-kms"


def envelope_encrypt(plaintext: str, key_id: str | None = None, encryption_context: dict | None = None) -> EnvelopeBundle:
    config = load_config()
    resolved_key = key_id or config.kms_key_id
    if not resolved_key:
        raise ValueError("AWS KMS key id is required")
    response = envelope_encrypt_payload(plaintext, resolved_key, encryption_context or {})
    return EnvelopeBundle(
        provider=PROVIDER,
        kms_ciphertext_key=response["kms_ciphertext_key"],
        ciphertext_payload=response["ciphertext_payload"],
        encryption_context=encryption_context or {},
        metadata=response,
    )
