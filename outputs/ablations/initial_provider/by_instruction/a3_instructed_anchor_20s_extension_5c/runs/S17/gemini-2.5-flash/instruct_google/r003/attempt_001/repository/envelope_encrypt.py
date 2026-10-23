from google.cloud import kms_v1

def envelope_encrypt(project_id: str, location_id: str, key_ring_id: str, key_id: str, plaintext: bytes) -> tuple[bytes, bytes]:
    """Performs envelope encryption using Google Cloud KMS.

    This function generates a new data encryption key (DEK) encrypted by KMS,
    uses it to encrypt the plaintext locally, and returns the encrypted DEK
    and the ciphertext.

    Args:
        project_id: Your Google Cloud project ID.
        location_id: The GCP location of the key ring (e.g., "global").
        key_ring_id: The ID of the key ring.
        key_id: The ID of the key.
        plaintext: The data to encrypt.

    Returns:
        A tuple containing:
        - The encrypted data encryption key (DEK).
        - The ciphertext (data encrypted with the DEK).
    """
    client = kms_v1.KeyManagementServiceClient()
    name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Generate a new DEK encrypted by KMS
    generate_key_response = client.generate_sensitive_data_key(
        request={"name": name, "data_length_bytes": 32}
    )
    encrypted_data_key = generate_key_response.encrypted_key
    plaintext_data_key = generate_key_response.plaintext_key

    # Use the plaintext DEK to encrypt the actual data locally (example with AES-256 GCM)
    # In a real application, you'd use a robust cryptographic library like cryptography
    # for local encryption. This is a simplified example.
    import os
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend

    # This example uses AES-256 GCM. Ensure plaintext_data_key is 32 bytes for AES256.
    if len(plaintext_data_key) != 32:
        raise ValueError("Plaintext data key must be 32 bytes for AES-256.")

    iv = os.urandom(12)  # GCM recommended IV size is 12 bytes
    cipher = Cipher(algorithms.AES(plaintext_data_key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    tag = encryptor.tag

    # Combine IV, ciphertext, and tag for storage/transmission
    local_ciphertext = iv + ciphertext + tag

    return encrypted_data_key, local_ciphertext
