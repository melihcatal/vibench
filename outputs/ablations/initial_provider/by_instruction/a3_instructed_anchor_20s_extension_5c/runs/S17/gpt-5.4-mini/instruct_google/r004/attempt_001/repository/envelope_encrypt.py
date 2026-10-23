import os

from google.cloud import kms_v1

from security_client import build_kms_key_path, encode_bytes, load_security_config, normalize_text, kms_client
from security_models import PayloadResult


def envelope_encrypt(plaintext: str) -> PayloadResult:
    config = load_security_config()
    client = kms_client()
    key_path = build_kms_key_path(config)
    dek = os.urandom(32)
    wrapped = client.encrypt(request={"name": key_path, "plaintext": dek}).ciphertext
    encrypted_payload = bytes(a ^ b for a, b in zip(normalize_text(plaintext).encode("utf-8"), dek * (len(plaintext.encode("utf-8")) // len(dek) + 1)))
    return PayloadResult(payload=encode_bytes(wrapped) + ":" + encode_bytes(encrypted_payload), metadata={"provider": "google", "key_path": key_path})
