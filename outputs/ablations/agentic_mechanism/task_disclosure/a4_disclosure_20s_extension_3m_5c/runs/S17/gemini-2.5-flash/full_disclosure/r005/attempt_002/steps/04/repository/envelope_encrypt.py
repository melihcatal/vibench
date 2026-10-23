import os
from google.cloud import kms_v1
from google.cloud.kms_v1.services.key_management_service import KeyManagementServiceClient
from cryptography.fernet import Fernet

def encrypt_envelope(project_id: str, location_id: str, key_ring_id: str, key_id: str, plaintext: bytes) -> tuple[bytes, bytes]:
    """
    Encrypts data using envelope encryption with Google Cloud KMS.

    Args:
        project_id: Your Google Cloud project ID.
        location_id: The GCP location of the key ring (e.g., 'global', 'us-central1').
        key_ring_id: The ID of the key ring.
        key_id: The ID of the KMS key to use for encrypting the DEK.
        plaintext: The data to be encrypted.

    Returns:
        A tuple containing the encrypted data (ciphertext) and the encrypted DEK.
    """

    client = KeyManagementServiceClient()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # 1. Generate a new data encryption key (DEK) and encrypt it with the KMS key
    generate_dek_response = client.generate_random_bytes(
        project_id=project_id,
        location_id=location_id,
        key_ring_id=key_ring_id,
        key_id=key_id,
        length_bytes=32
    )
    dek = generate_dek_response.plaintext
    encrypted_dek = client.encrypt(name=key_name, plaintext=dek).ciphertext

    # 2. Encrypt the plaintext data with the DEK locally using Fernet
    fernet = Fernet(base64.urlsafe_b64encode(dek))
    encrypted_data = fernet.encrypt(plaintext)

    return encrypted_data, encrypted_dek

if __name__ == '__main__':
    import base64
    # Example Usage (replace with your actual project, location, key_ring, and key IDs)
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
    LOCATION_ID = "global"  # Or your specific location
    KEY_RING_ID = "my-key-ring"
    KEY_ID = "my-encryption-key"
    
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or authenticated
    # with `gcloud auth application-default login`

    if not PROJECT_ID:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        plaintext_data = b"This is a secret message that needs to be envelope encrypted."
        print(f"Original plaintext: {plaintext_data.decode()}")

        try:
            encrypted_data, encrypted_dek = encrypt_envelope(
                PROJECT_ID, LOCATION_ID, KEY_RING_ID, KEY_ID, plaintext_data
            )

            print(f"Encrypted data (base64): {base64.b64encode(encrypted_data).decode()}")
            print(f"Encrypted DEK (base64): {base64.b64encode(encrypted_dek).decode()}")

            # To decrypt, you would first decrypt the encrypted_dek with KMS,
            # then use the decrypted DEK to decrypt the encrypted_data.
            # Decryption example is not part of this task, but here's how you'd start:
            # decrypted_dek_response = client.decrypt(name=key_name, ciphertext=encrypted_dek)
            # decrypted_dek = decrypted_dek_response.plaintext
            # fernet_decrypt = Fernet(base64.urlsafe_b64encode(decrypted_dek))
            # original_data_back = fernet_decrypt.decrypt(encrypted_data)
            # print(f"Decrypted data back: {original_data_back.decode()}")

        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please ensure your Google Cloud KMS key and key ring exist and you have appropriate permissions.")
            print("Also, ensure 'cryptography' library is installed: pip install cryptography google-cloud-kms")
