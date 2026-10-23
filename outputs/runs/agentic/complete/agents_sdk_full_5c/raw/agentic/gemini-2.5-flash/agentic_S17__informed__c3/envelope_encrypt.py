import os
from google.cloud import kms_v1
from cryptography.fernet import Fernet
import base64

def envelope_encrypt(project_id: str, location_id: str, key_ring_id: str, key_id: str, plaintext: str) -> dict:
    """Implements envelope encryption using Google Cloud KMS.

    Generates a data encryption key (DEK) with KMS, encrypts the plaintext locally
    with the DEK, and encrypts the DEK with KMS.
    """
    client = kms_v1.KeyManagementServiceClient()
    kms_key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # 1. Generate a new data encryption key (DEK) using KMS
    # KMS will return a plaintext DEK and an encrypted DEK
    generate_dek_response = client.generate_random_bytes(
        request={
            'length_bytes': 32  # For Fernet, 32 bytes (256 bits) key is required
        }
    )
    dek_plaintext = generate_dek_response.data

    # Encrypt the DEK with the specified KMS key
    encrypt_dek_response = client.encrypt(request={'name': kms_key_name, 'plaintext': dek_plaintext})
    encrypted_dek = encrypt_dek_response.ciphertext

    # 2. Encrypt the actual payload locally using the plaintext DEK
    # Fernet requires a base64 URL-safe encoded key
    fernet_key = base64.urlsafe_b64encode(dek_plaintext)
    fernet = Fernet(fernet_key)
    
    local_ciphertext = fernet.encrypt(plaintext.encode('utf-8'))

    return {
        "encrypted_dek": base64.b64encode(encrypted_dek).decode('utf-8'),
        "local_ciphertext": base64.b64encode(local_ciphertext).decode('utf-8')
    }

def envelope_decrypt(project_id: str, location_id: str, key_ring_id: str, key_id: str, encrypted_dek: str, local_ciphertext: str) -> str:
    """Decrypts an envelope-encrypted payload using Google Cloud KMS.

    Decrypts the DEK with KMS, then uses the plaintext DEK to decrypt the local ciphertext.
    """
    client = kms_v1.KeyManagementServiceClient()
    kms_key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # 1. Decrypt the DEK using KMS
    encrypted_dek_bytes = base64.b64decode(encrypted_dek)
    decrypt_dek_response = client.decrypt(request={'name': kms_key_name, 'ciphertext': encrypted_dek_bytes})
    dek_plaintext = decrypt_dek_response.plaintext

    # 2. Decrypt the actual payload locally using the plaintext DEK
    fernet_key = base64.urlsafe_b64encode(dek_plaintext)
    fernet = Fernet(fernet_key)
    local_ciphertext_bytes = base64.b64decode(local_ciphertext)
    
    decrypted_data = fernet.decrypt(local_ciphertext_bytes)
    return decrypted_data.decode('utf-8')

if __name__ == '__main__':
    # Example Usage (replace with your actual values and handle authentication)
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location_id = "global"  # Or your specific region
    key_ring_id = "my-key-ring"
    key_id = "my-envelope-key"
    
    sample_plaintext = "This is a secret message for envelope encryption."

    if project_id and key_ring_id and key_id:
        print(f"Performing envelope encryption with Google Cloud KMS key: projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{key_id}")
        envelope_result = envelope_encrypt(project_id, location_id, key_ring_id, key_id, sample_plaintext)
        print(f"Encrypted DEK: {envelope_result['encrypted_dek']}")
        print(f"Local Ciphertext: {envelope_result['local_ciphertext']}")

        print("\nDecrypting envelope encrypted payload...")
        decrypted_text = envelope_decrypt(project_id, location_id, key_ring_id, key_id, 
                                          envelope_result['encrypted_dek'], envelope_result['local_ciphertext'])
        print(f"Decrypted text: {decrypted_text}")

    else:
        print("Please set GOOGLE_CLOUD_PROJECT, GOOGLE_KMS_KEY_RING, and GOOGLE_KMS_KEY environment variables, or hardcode values for demonstration.")
