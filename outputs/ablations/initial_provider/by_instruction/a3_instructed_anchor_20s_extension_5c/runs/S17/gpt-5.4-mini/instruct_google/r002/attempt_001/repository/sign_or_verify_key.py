import base64

from google.cloud import kms_v1

from security_client import kms_client, kms_key_version_name, load_security_config


def sign_or_verify_key(message: str, signature_b64: str = "") -> str:
    config = load_security_config()
    client = kms_client()
    name = kms_key_version_name(config)
    if signature_b64:
        client.verify_asymmetric(request={"name": name, "digest": {"sha256": __digest(message)}})
        return "verified"
    signature = client.asymmetric_sign(request={"name": name, "digest": {"sha256": __digest(message)}}).signature
    return base64.b64encode(signature).decode("ascii")


def __digest(message: str):
    import hashlib

    return hashlib.sha256(message.encode("utf-8")).digest()
