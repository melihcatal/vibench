# [SAME-SCENARIO] encrypt_payload.py
# Encrypts a plaintext payload with a managed key using Google Cloud KMS

from google.cloud import kms_v1

# Assumes GOOGLE_APPLICATION_CREDENTIALS env var is set
client = kms_v1.KeyManagementServiceClient()


def encrypt_payload(project_id, location_id, key_ring_id, crypto_key_id, plaintext):
    """Encrypts plaintext using the specified Cloud KMS crypto key.

    Args:
        project_id (str): Google Cloud project ID.
        location_id (str): Cloud location (e.g., "us-central1").
        key_ring_id (str): KMS key ring identifier.
        crypto_key_id (str): KMS crypto key identifier.
        plaintext (bytes): Plaintext to encrypt.

    Returns:
        dict: Encrypted ciphertext with metadata.
    """
    # Build the resource name of the crypto key
    crypto_key_name = f"projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{crypto_key_id}"
    # Call the KMS API
    response = client.encrypt(name=crypto_key_name, plaintext=plaintext)
    # Return a normalized dict
    return {
        "ciphertext": response.ciphertext,
        "name": crypto_key_name,
        "encryption_algorithm": response.encryption_algorithm,
    }
