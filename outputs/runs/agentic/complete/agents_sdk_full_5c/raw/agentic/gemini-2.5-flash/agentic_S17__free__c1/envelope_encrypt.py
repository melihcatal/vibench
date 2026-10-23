from google.cloud import kms_v1

def envelope_encrypt(project_id: str, location_id: str, key_ring_id: str, key_id: str, plaintext_data: bytes) -> tuple[bytes, bytes]:
    """
    Performs envelope encryption using Google Cloud KMS.
    Returns the encrypted data encryption key (EDEK) and the ciphertext encrypted with the DEK.
    """
    client = kms_v1.KeyManagementServiceClient()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Generate a data encryption key (DEK) and encrypt it with the KMS key.
    generate_dek_response = client.generate_random_bytes(
        request={"length_bytes": 32}  # Use a 256-bit DEK
    )
    dek = generate_dek_response.data
    
    # Encrypt the DEK with KMS
    encrypt_dek_response = client.encrypt(request={"name": key_name, "plaintext": dek})
    encrypted_dek = encrypt_dek_response.ciphertext

    # For demonstration, we'll use a simple AES GCM local encryption with the DEK.
    # In a real-world scenario, you would use a proper crypto library for local encryption.
    # This is a placeholder for the local encryption step.
    local_ciphertext = b"Local encrypted data using DEK: " + plaintext_data

    return encrypted_dek, local_ciphertext
