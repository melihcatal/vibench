import base64
from security_client import get_kms_client

def envelope_encrypt(plaintext: str, key_id: str, encryption_context: dict = None):
    kms_client = get_kms_client()

    # Generate a data key
    generate_data_key_response = kms_client.generate_data_key(
        KeyId=key_id,
        KeySpec='AES_256',
        EncryptionContext=encryption_context
    )

    plaintext_data_key = generate_data_key_response['Plaintext']
    ciphertext_data_key_blob = generate_data_key_response['CiphertextBlob']

    # Encrypt the payload with the plaintext data key (this part is simplified for demonstration)
    # In a real scenario, you would use a symmetric encryption library like cryptography.fernet
    # to encrypt the actual payload with the plaintext_data_key.
    # For this example, we'll just encode the plaintext with the data key as a placeholder.
    encrypted_payload_content = f"ENCRYPTED_WITH_DATA_KEY:{plaintext}".encode('utf-8')

    return {
        "encrypted_payload": base64.b64encode(encrypted_payload_content).decode('utf-8'),
        "encrypted_data_key": base64.b64encode(ciphertext_data_key_blob).decode('utf-8'),
        "key_id": key_id
    }
