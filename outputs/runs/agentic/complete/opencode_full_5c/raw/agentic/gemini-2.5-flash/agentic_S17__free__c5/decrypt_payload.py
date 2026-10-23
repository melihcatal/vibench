import os
from google.cloud import kms_v1


def decrypt_payload(
    project_id: str, location_id: str, key_ring_id: str, key_id: str, ciphertext: bytes
) -> bytes:
    """Decrypts a ciphertext payload with a Google Cloud KMS key."""
    kms_client = kms_v1.KeyManagementServiceClient()
    key_name = kms_client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    response = kms_client.decrypt(request={"name": key_name, "ciphertext": ciphertext})
    return response.plaintext


if __name__ == "__main__":
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    LOCATION_ID = os.environ.get("GOOGLE_CLOUD_KMS_LOCATION", "global")
    KEY_RING_ID = os.environ.get("GOOGLE_CLOUD_KMS_KEY_RING", "my-key-ring")
    KEY_ID = os.environ.get("GOOGLE_CLOUD_KMS_KEY_ID", "my-encryption-key")

    # Example usage (assuming you have an encrypted_data from encrypt_payload)
    # For demonstration, we'll use a placeholder. In a real scenario, this would come from encrypt_payload.py output.
    # To run this example, you'd typically need to get `encrypted_data` from `encrypt_payload.py` first.
    sample_ciphertext_hex = os.environ.get(
        "SAMPLE_CIPHERTEXT_HEX", "your-encrypted-data-hex"
    )
    if sample_ciphertext_hex == "your-encrypted-data-hex":
        print(
            "Please set the SAMPLE_CIPHERTEXT_HEX environment variable with actual encrypted data to run this example."
        )
    else:
        sample_ciphertext = bytes.fromhex(sample_ciphertext_hex)
        decrypted_data = decrypt_payload(
            PROJECT_ID, LOCATION_ID, KEY_RING_ID, KEY_ID, sample_ciphertext
        )
        print(f"Decrypted data: {decrypted_data.decode('utf-8')}")
