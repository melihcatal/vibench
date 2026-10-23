from security_client import KMSClient
from security_models import denormalize_base64, deserialize_payload


def decrypt_payload(ciphertext: str) -> dict:
    client = KMSClient()
    ciphertext_bytes = denormalize_base64(ciphertext)
    plaintext_bytes = client.decrypt(ciphertext_bytes)
    return {
        "plaintext": deserialize_payload(plaintext_bytes),
        "key_id": client.key_id,
        "algorithm": "AES_256_GCM",
    }
