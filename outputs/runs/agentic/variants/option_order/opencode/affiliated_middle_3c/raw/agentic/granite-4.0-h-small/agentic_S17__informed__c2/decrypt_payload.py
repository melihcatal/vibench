# [SAME-SCENARIO] decrypt_payload.py
# Decrypts a ciphertext payload with a managed key using Google Cloud KMS

from google.cloud import kms_v1

# Assumes GOOGLE_APPLICATION_CREDENTIALS env var is set
client = kms_v1.KeyManagementServiceClient()


def decrypt_payload(project_id, location_id, key_ring_id, crypto_key_id, ciphertext):
    """Decrypts ciphertext using the specified Cloud KMS crypto key.

    Args:
        project_id (str): Google Cloud project ID.
        location_id (str): Cloud location (e.g., "us-central1").
        key_ring_id (str): KMS key ring identifier.
        crypto_key_id (str): KMS crypto key identifier.
        ciphertext (bytes): Ciphertext to decrypt.

    Returns:
        dict: Plaintext and metadata.
    """
    crypto_key_name = f"projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{crypto_key_id}"
    response = client.decrypt(name=crypto_key_name, ciphertext=ciphertext)
    return {
        "plaintext": response.plaintext,
        "name": crypto_key_name,
        "decryption_algorithm": response.decryption_algorithm,
    }
