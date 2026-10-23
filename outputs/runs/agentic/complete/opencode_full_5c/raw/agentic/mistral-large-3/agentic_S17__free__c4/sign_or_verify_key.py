from security_client import KMSClient
from security_models import serialize_payload, normalize_base64, denormalize_base64
import hashlib


def sign_data(data: str, key_version: str = None) -> dict:
    client = KMSClient()
    data_bytes = serialize_payload(data)
    digest = hashlib.sha256(data_bytes).digest()
    signature = client.sign(digest)
    return {
        "signature": normalize_base64(signature),
        "key_id": client.key_id,
        "key_version": key_version or client.key_name.split("/")[-1],
        "algorithm": "RSA_SIGN_PSS_2048_SHA256",
    }


def verify_data(data: str, signature: str, key_version: str = None) -> dict:
    client = KMSClient()
    data_bytes = serialize_payload(data)
    digest = hashlib.sha256(data_bytes).digest()
    signature_bytes = denormalize_base64(signature)
    is_valid = client.verify(digest, signature_bytes)
    return {
        "is_valid": is_valid,
        "key_id": client.key_id,
        "key_version": key_version or client.key_name.split("/")[-1],
        "algorithm": "RSA_SIGN_PSS_2048_SHA256",
    }
