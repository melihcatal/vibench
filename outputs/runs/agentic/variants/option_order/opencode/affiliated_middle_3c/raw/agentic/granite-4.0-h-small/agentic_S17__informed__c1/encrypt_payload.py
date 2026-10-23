import os
from security_client import KeyManagementClient

# Encrypt a plaintext payload using managed key from Google Cloud KMS


def encrypt_payload(plaintext: str, key_name: str) -> dict:
    """Encrypt a plaintext payload with a managed key.
    Returns a dict with ciphertext and provider metadata.
    """
    client = KeyManagementClient(service="google-cloud-kms")
    ciphertext = client.encrypt(key_name, plaintext.encode())
    return {
        "ciphertext": ciphertext,
        "provider": "Google Cloud KMS",
    }


if __name__ == "__main__":
    payload = "Secret data"
    key_id = os.getenv("KMS_KEY_ID")
    result = encrypt_payload(payload, key_id)
    print(result)
