from google.cloud import kms_v1
import os

def decrypt_payload(project_id, location_id, key_ring_id, key_id, ciphertext):
    """Decrypts a ciphertext payload with Google Cloud KMS."""

    client = kms_v1.KeyManagementServiceClient()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Convert ciphertext to bytes if it's not already
    if isinstance(ciphertext, str):
        ciphertext_bytes = ciphertext.encode('utf-8')
    else:
        ciphertext_bytes = ciphertext

    response = client.decrypt(request={'name': key_name, 'ciphertext': ciphertext_bytes})
    return response.plaintext.decode('utf-8')

if __name__ == '__main__':
    # Replace with your actual project, location, key ring, and key IDs
    PROJECT_ID = os.environ.get('GCP_PROJECT_ID')
    LOCATION_ID = 'global'  # Or your specific location, e.g., 'us-central1'
    KEY_RING_ID = os.environ.get('GCP_KMS_KEY_RING_ID')
    KEY_ID = os.environ.get('GCP_KMS_KEY_ID')

    # Example ciphertext (replace with your actual ciphertext)
    # This should be a base64-encoded string of the encrypted data
    EXAMPLE_CIPHERTEXT = os.environ.get('EXAMPLE_CIPHERTEXT')

    if not all([PROJECT_ID, KEY_RING_ID, KEY_ID, EXAMPLE_CIPHERTEXT]):
        print("Please set the environment variables: GCP_PROJECT_ID, GCP_KMS_KEY_RING_ID, GCP_KMS_KEY_ID, and EXAMPLE_CIPHERTEXT")
    else:
        try:
            decrypted_text = decrypt_payload(PROJECT_ID, LOCATION_ID, KEY_RING_ID, KEY_ID, EXAMPLE_CIPHERTEXT)
            print("Decrypted payload:", decrypted_text)
        except Exception as e:
            print(f"Error decrypting payload: {e}")
