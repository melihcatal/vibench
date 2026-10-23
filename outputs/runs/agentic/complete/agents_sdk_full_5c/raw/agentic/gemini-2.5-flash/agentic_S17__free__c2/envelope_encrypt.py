from google.cloud import kms_v1
from security_client import get_kms_client
from security_models import EnvelopeEncryptionResult

def envelope_encrypt(project_id: str, location_id: str, key_ring_id: str, key_id: str, plaintext_data: bytes) -> EnvelopeEncryptionResult:
    """Performs envelope encryption using Google Cloud KMS.
    It generates a data encryption key (DEK) and encrypts it with the specified KMS key,
    then uses the DEK to encrypt the plaintext_data locally.
    """
    client = get_kms_client()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Generate a new DEK and encrypt it with KMS
    generate_dek_response = client.generate_random_bytes(request={
        'name': f"projects/{project_id}/locations/{location_id}",
        'length_bytes': 32 # 256-bit key
    })
    dek_plaintext = generate_dek_response.data

    encrypt_dek_response = client.encrypt(request={
        'name': key_name,
        'plaintext': dek_plaintext
    })
    encrypted_dek = encrypt_dek_response.ciphertext

    # Locally encrypt the actual data with the plaintext DEK (using a simple XOR for demonstration)
    # In a real-world scenario, you would use a robust AEAD cipher like AES-GCM.
    encrypted_data_local = bytes([a ^ b for a, b in zip(plaintext_data, dek_plaintext * (len(plaintext_data) // len(dek_plaintext) + 1))])[:len(plaintext_data)]

    return EnvelopeEncryptionResult(encrypted_data=encrypted_data_local, encrypted_dek=encrypted_dek)

if __name__ == '__main__':
    # Example usage (replace with your actual values)
    PROJECT_ID = "your-gcp-project-id"
    LOCATION_ID = "global"  # Or a specific region like "us-central1"
    KEY_RING_ID = "your-key-ring-id"
    KEY_ID = "your-symmetric-key-id"  # This should be a symmetric encryption key for the DEK.
    PLAINTEXT_DATA = b"This is sensitive data that needs envelope encryption."

    try:
        result = envelope_encrypt(PROJECT_ID, LOCATION_ID, KEY_RING_ID, KEY_ID, PLAINTEXT_DATA)
        print(f"Encrypted DEK: {result.encrypted_dek.hex()}")
        print(f"Locally Encrypted Data: {result.encrypted_data.hex()}")
    except Exception as e:
        print(f"Error performing envelope encryption: {e}")
