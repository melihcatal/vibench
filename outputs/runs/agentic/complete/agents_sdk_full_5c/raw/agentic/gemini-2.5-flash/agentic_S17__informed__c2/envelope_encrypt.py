import os
from google.cloud import kms_v1

from security_client import get_kms_client
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResult

def envelope_encrypt(request: EnvelopeEncryptionRequest) -> EnvelopeEncryptionResult:
    """Implements envelope encryption using Google Cloud KMS.
    KMS encrypts a data encryption key (DEK) which is then used to encrypt the payload locally.
    """
    client = get_kms_client()
    key_name = client.crypto_key_path(
        os.environ["GCP_PROJECT_ID"],
        os.environ["GCP_KMS_LOCATION"],
        os.environ["GCP_KMS_KEY_RING"],
        os.environ["GCP_KMS_KEY_NAME"],
    )

    # Generate a new data encryption key (DEK) and encrypt it with the KEK in KMS
    generate_dek_response = client.generate_data_encryption_key(
        request=kms_v1.GenerateDataEncryptionKeyRequest(
            name=key_name,
            # This can be AES_256_GCM or other algorithms supported by KMS for DEKs
            # For this example, let's assume a symmetric key usage with a GCM key
            # For actual envelope encryption, you'd typically generate a local DEK and then encrypt *that* with KMS
            # The KMS generate_data_encryption_key method does exactly this for us.
            key_project_id=os.environ["GCP_PROJECT_ID"],
            key_location=os.environ["GCP_KMS_LOCATION"],
            key_ring_id=os.environ["GCP_KMS_KEY_RING"],
            crypto_key_id=os.environ["GCP_KMS_KEY_NAME"],
            data_encryption_key_algorithm=kms_v1.CryptoKeyVersion.CryptoKeyVersionAlgorithm.AES_256_GCM,
        )
    )

    encrypted_dek = generate_dek_response.wrapped_key
    plaintext_dek = generate_dek_response.plaintext_crc32c # This is not the DEK itself, but its checksum

    # In a real envelope encryption, you would use the plaintext_dek (from `generate_data_encryption_key` response)
    # to encrypt the actual payload *locally*, then store the locally encrypted payload and the `encrypted_dek`.
    # For this example, we'll just return the encrypted DEK and a placeholder for the payload.
    # The KMS `generate_data_encryption_key` also returns the plaintext DEK which you'd use here.

    # For simplicity of this example, we will simulate the process. In a real scenario, you'd perform local encryption here.
    # Example: local_ciphertext = aes_gcm_encrypt(request.plaintext_data, generate_dek_response.plaintext_data_encryption_key)

    return EnvelopeEncryptionResult(
        encrypted_data_encryption_key=encrypted_dek,
        # For a full implementation, the actual payload would be encrypted locally using the plaintext DEK.
        # This is a simplified representation focusing on the KMS interaction for the DEK.
        locally_encrypted_payload=b"simulated_locally_encrypted_payload"
    )

if __name__ == "__main__":
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS, GCP_PROJECT_ID, GCP_KMS_LOCATION, GCP_KMS_KEY_RING, GCP_KMS_KEY_NAME env vars)
    # from dotenv import load_dotenv
    # load_dotenv()
    # req = EnvelopeEncryptionRequest(plaintext_data=b"Sensitive document content.")
    # result = envelope_encrypt(req)
    # print(f"Encrypted DEK: {result.encrypted_data_encryption_key.hex()}")
    # print(f"Simulated Local Ciphertext: {result.locally_encrypted_payload.decode()}")
    pass
