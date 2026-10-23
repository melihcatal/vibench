from google.cloud import kms
from security_models import EnvelopeEncryptionConfig
from security_client import get_kms_client

def envelope_encrypt(payload: dict, config: EnvelopeEncryptionConfig):
    client = get_kms_client()
    name = client.crypto_key_path(
        config.project_id, config.location, config.key_ring, config.key_id
    )

    # Generate a new data encryption key (DEK) and encrypt it with the KEK
    generate_response = client.generate_random_bytes(length_bytes=32)
    dek = generate_response.data

    encrypt_dek_response = client.encrypt(
        request={"name": name, "plaintext": dek}
    )
    encrypted_dek = encrypt_dek_response.ciphertext

    # In a real scenario, you would use the DEK to encrypt the actual data
    # For this example, we will just return the encrypted DEK and the DEK itself (for demonstration)
    return {"encrypted_dek": encrypted_dek, "plaintext_dek": dek.hex()}
