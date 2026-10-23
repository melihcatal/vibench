from google.cloud import kms_v1
import os

def envelope_encrypt(project_id: str, location_id: str, key_ring_id: str, key_id: str) -> tuple[bytes, bytes]:
    """Performs envelope encryption by generating a data encryption key (DEK)
    and encrypting it with a Google Cloud KMS key (KEK). Returns the encrypted DEK and the raw DEK.
    The raw DEK would then be used to encrypt the actual payload locally.
    """
    client = kms_v1.KeyManagementServiceClient()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Generate a new DEK and encrypt it with the specified KEK
    generate_response = client.generate_data_encryption_key(
        request={
            "name": key_name,
            "key_algorithm": kms_v1.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
        }
    )

    encrypted_dek = generate_response.wrapped_key
    plaintext_dek = generate_response.plaintext

    return encrypted_dek, plaintext_dek

if __name__ == '__main__':
    # Example usage:
    # project_id = "your-gcp-project-id"
    # location_id = "global"
    # key_ring_id = "your-key-ring-id"
    # key_id = "your-key-id"
    #
    # encrypted_dek, plaintext_dek = envelope_encrypt(project_id, location_id, key_ring_id, key_id)
    # print(f"Encrypted DEK: {encrypted_dek.hex()}")
    # print(f"Plaintext DEK (to be used locally): {plaintext_dek.hex()}")
    pass
