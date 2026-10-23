from google.cloud import kms_v1

from security_client import build_kms_key_path, decode_bytes, load_security_config, normalize_text, kms_client
from security_models import PayloadResult


def decrypt_payload(ciphertext: str) -> PayloadResult:
    config = load_security_config()
    client = kms_client()
    key_path = build_kms_key_path(config)
    response = client.decrypt(request={"name": key_path, "ciphertext": decode_bytes(normalize_text(ciphertext))})
    return PayloadResult(payload=response.plaintext.decode("utf-8"), metadata={"provider": "google", "key_path": key_path})
