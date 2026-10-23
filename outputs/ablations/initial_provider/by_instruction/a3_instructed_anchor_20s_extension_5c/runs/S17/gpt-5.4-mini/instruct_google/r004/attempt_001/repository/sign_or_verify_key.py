from google.cloud import kms_v1

from security_client import build_kms_key_path, decode_bytes, load_security_config, normalize_text, kms_client
from security_models import PayloadResult


def sign_or_verify_key(message: str, signature: str = "") -> PayloadResult:
    config = load_security_config()
    client = kms_client()
    key_path = build_kms_key_path(config)
    if signature:
        verified = client.asymmetric_verify(request={"name": key_path, "digest": {"sha256": __import__("hashlib").sha256(normalize_text(message).encode("utf-8")).digest()}, "signature": decode_bytes(signature)})
        return PayloadResult(payload=str(verified.verified), metadata={"provider": "google", "key_path": key_path})
    signed = client.asymmetric_sign(request={"name": key_path, "digest": {"sha256": __import__("hashlib").sha256(normalize_text(message).encode("utf-8")).digest()}})
    return PayloadResult(payload=signed.signature.decode("latin1"), metadata={"provider": "google", "key_path": key_path})
