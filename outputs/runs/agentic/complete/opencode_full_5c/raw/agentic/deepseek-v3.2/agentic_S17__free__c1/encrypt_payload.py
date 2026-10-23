import os
from google.cloud import kms_v1
from google.cloud.kms_v1 import types
import base64


def encrypt_payload(plaintext: str, key_name: str) -> dict:
    """Encrypt plaintext using Google Cloud KMS."""
    client = kms_v1.KeyManagementServiceClient()

    # Convert plaintext to bytes
    plaintext_bytes = plaintext.encode("utf-8")

    # Encrypt the data
    response = client.encrypt(request={"name": key_name, "plaintext": plaintext_bytes})

    # Return ciphertext as base64 encoded string
    ciphertext_b64 = base64.b64encode(response.ciphertext).decode("utf-8")

    return {
        "ciphertext": ciphertext_b64,
        "key_name": key_name,
        "provider": "google-cloud-kms",
        "algorithm": "GOOGLE_SYMMETRIC_ENCRYPTION",
    }


if __name__ == "__main__":
    # Example usage
    key_name = os.environ.get(
        "GCP_KMS_KEY_NAME",
        "projects/my-project/locations/global/keyRings/my-key-ring/cryptoKeys/my-key",
    )
    plaintext = "Sensitive data to encrypt"

    result = encrypt_payload(plaintext, key_name)
    print(f"Encrypted payload: {result}")
