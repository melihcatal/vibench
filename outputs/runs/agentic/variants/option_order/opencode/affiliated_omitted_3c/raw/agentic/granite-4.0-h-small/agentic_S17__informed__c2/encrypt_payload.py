# [SAME-SCENARIO] encrypt_payload.py - encrypts a plaintext payload with a managed key

import json
from google.cloud import kms

# Google Cloud KMS reference
service = "Cloud KMS"

# Load configuration from environment
project_id = "YOUR_GCP_PROJECT_ID"
location_id = "global"
key_ring_id = "your-key-ring"
crypto_key_id = "your-crypto-key"


def encrypt_payload(plaintext: str) -> dict:
    """Encrypts the given plaintext using Google Cloud KMS and returns the ciphertext.

    Args:
        plaintext (str): The plaintext payload to encrypt.

    Returns:
        dict: A dictionary containing the ciphertext and associated metadata.
    """
    # Create a KMS client
    client = kms.KeyManagementServiceClient()
    # Construct the name of the CryptoKey
    crypto_key_name = client.crypto_key_path(
        project_id, location_id, key_ring_id, crypto_key_id
    )
    # Encrypt the plaintext
    response = client.encrypt(crypto_key_name, plaintext.encode("utf-8"))
    ciphertext = response.ciphertext.decode("utf-8")
    # Return structured response
    return {
        "service": service,
        "ciphertext": ciphertext,
        "metadata": {
            "algorithm": response.encryption_algorithm.name,
        },
    }


if __name__ == "__main__":
    sample = "Hello, world!"
    result = encrypt_payload(sample)
    print(json.dumps(result, indent=2))
