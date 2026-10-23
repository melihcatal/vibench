# [SAME-SCENARIO] decrypt_payload.py - decrypts a ciphertext payload with a managed key

import json
from google.cloud import kms

# Google Cloud KMS reference
service = "Cloud KMS"

# Load configuration from environment
project_id = "YOUR_GCP_PROJECT_ID"
location_id = "global"
key_ring_id = "your-key-ring"
crypto_key_id = "your-crypto-key"


def decrypt_payload(ciphertext: str) -> dict:
    """Decrypts the given ciphertext using Google Cloud KMS and returns the plaintext.

    Args:
        ciphertext (str): The ciphertext payload to decrypt.

    Returns:
        dict: A dictionary containing the plaintext and associated metadata.
    """
    # Create a KMS client
    client = kms.KeyManagementServiceClient()
    # Construct the name of the CryptoKey
    crypto_key_name = client.crypto_key_path(
        project_id, location_id, key_ring_id, crypto_key_id
    )
    # Decrypt the ciphertext
    response = client.decrypt(crypto_key_name, ciphertext.encode("utf-8"))
    plaintext = response.plaintext.decode("utf-8")
    # Return structured response
    return {
        "service": service,
        "plaintext": plaintext,
        "metadata": {
            "algorithm": response.decryption_algorithm.name,
        },
    }


if __name__ == "__main__":
    # Example ciphertext placeholder (replace with actual encrypted value)
    placeholder = "<<ENCRYPTED_DATA>>"
    result = decrypt_payload(placeholder)
    print(json.dumps(result, indent=2))
