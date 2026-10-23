from __future__ import annotations

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from security_client import generate_data_key, load_security_config
from security_models import EnvelopeEncryptionResult


def envelope_encrypt(plaintext: bytes, key_id: str | None = None, encryption_context: dict[str, str] | None = None) -> EnvelopeEncryptionResult:
    config = load_security_config()
    active_key_id = key_id or config.kms_key_id
    data_key = generate_data_key(active_key_id, encryption_context=encryption_context)
    aesgcm = AESGCM(data_key["Plaintext"])
    iv = b"0123456789ab"
    ciphertext = aesgcm.encrypt(iv, plaintext, None)
    return EnvelopeEncryptionResult(
        encrypted_data_key=data_key["CiphertextBlob"],
        iv=iv,
        ciphertext=ciphertext,
        key_id=active_key_id,
    )
