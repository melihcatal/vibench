from google.cloud import kms_v1
from cryptography.fernet import Fernet

def envelope_encrypt(project_id: str, location: str, key_ring: str, key_name: str, plaintext: bytes) -> tuple[bytes, bytes]:
    """Implements envelope encryption using Google Cloud KMS.

    Args:
        project_id: Your Google Cloud project ID.
        location: The Cloud KMS location (e.g., "global", "us-east1").
        key_ring: The Cloud KMS key ring name.
        key_name: The Cloud KMS key name.
        plaintext: The data to encrypt.

    Returns:
        A tuple containing the encrypted data key and the ciphertext.
    """
    client = kms_v1.KeyManagementServiceClient()
    key_path = client.crypto_key_path(project_id, location, key_ring, key_name)

    # Generate a new data encryption key (DEK) for local encryption
    dek = Fernet.generate_key()
    f = Fernet(dek)
    ciphertext = f.encrypt(plaintext)

    # Encrypt the DEK with Google Cloud KMS
    encrypt_dek_response = client.encrypt(request={"name": key_path, "plaintext": dek})
    encrypted_dek = encrypt_dek_response.ciphertext

    return encrypted_dek, ciphertext
