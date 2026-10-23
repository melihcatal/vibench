import os
from google.cloud import kms
from security_client import get_kms_client

def encrypt_payload(project_id, location_id, key_ring_id, crypto_key_id, plaintext, additional_data=b''):
    """Encrypts plaintext using Google Cloud KMS.
    Returns ciphertext (bytes).
    """
    client = get_kms_client()
    # Build the resource name of the crypto key
    key_name = f"projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{crypto_key_id}"
    # Encrypt request
    response = client.encrypt(
        name=key_name,
        plaintext=plaintext,
        additional_authenticated_data=additional_data,
    )
    return response.ciphertext

if __name__ == "__main__":
    # Example usage (credentials must be set via GOOGLE_APPLICATION_CREDENTIALS env var)
    project_id = os.getenv("GCLOUD_PROJECT")
    location_id = "global"
    key_ring_id = "my-key-ring"
    crypto_key_id = "my-key"
    plaintext = b"Secret message"
    ct = encrypt_payload(project_id, location_id, key_ring_id, crypto_key_id, plaintext)
    print("Ciphertext base64:", ct)
