from google.cloud import kms_v1

from security_client import build_kms_key_path, load_security_config, normalize_text, kms_client
from security_models import PayloadResult


def encrypt_payload(plaintext: str) -> PayloadResult:
    config = load_security_config()
    client = kms_client()
    key_path = build_kms_key_path(config)
    response = client.encrypt(request={"name": key_path, "plaintext": normalize_text(plaintext).encode("utf-8")})
    return PayloadResult(payload=response.ciphertext.decode("latin1"), metadata={"provider": "google", "key_path": key_path})
