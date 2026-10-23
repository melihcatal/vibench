import os
import base64
from google.cloud import kms_v1


def decrypt_payload(ciphertext_b64: str, key_name: str) -> dict:
    """Decrypt ciphertext using Google Cloud KMS."""
    client = kms_v1.KeyManagementServiceClient()

    # Decode base64 ciphertext
    ciphertext = base64.b64decode(ciphertext_b64)

    # Decrypt the data
    response = client.decrypt(request={"name": key_name, "ciphertext": ciphertext})

    # Convert decrypted bytes to string
    plaintext = response.plaintext.decode("utf-8")

    return {
        "plaintext": plaintext,
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
    ciphertext_b64 = "AQICAHh..."  # Example base64 ciphertext

    result = decrypt_payload(ciphertext_b64, key_name)
    print(f"Decrypted payload: {result}")
