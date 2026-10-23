import os
from google.cloud import kms
from security_client import get_kms_client

def decrypt_payload(project_id, location_id, key_ring_id, crypto_key_id, ciphertext, additional_data=b''):
    """Decrypts ciphertext using Google Cloud KMS.
    Returns plaintext (bytes).
    """
    client = get_kms_client()
    key_name = f"projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{crypto_key_id}"
    response = client.decrypt(
        name=key_name,
        ciphertext=ciphertext,
        additional_authenticated_data=additional_data,
    )
    return response.plaintext

if __name__ == "__main__":
    project_id = os.getenv("GCLOUD_PROJECT")
    location_id = "global"
    key_ring_id = "my-key-ring"
    crypto_key_id = "my-key"
    # ciphertext should be provided by encrypt_payload or elsewhere
    ct = b"YOUR_CIPHERTEXT_HERE"
    pt = decrypt_payload(project_id, location_id, key_ring_id, crypto_key_id, ct)
    print("Plaintext:", pt)
