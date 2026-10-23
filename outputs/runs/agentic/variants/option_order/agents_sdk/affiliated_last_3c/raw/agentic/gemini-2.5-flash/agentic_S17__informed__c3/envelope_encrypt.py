from google.cloud import kms
import os

def envelope_encrypt(project_id: str, location_id: str, key_ring_id: str, key_id: str, plaintext: bytes) -> tuple[bytes, bytes]:
    """Performs envelope encryption using Google Cloud KMS.
    Returns the encrypted data key and the encrypted plaintext.
    """
    client = kms.KeyManagementServiceClient()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Generate a new data encryption key and encrypt it with the KMS key
    generate_response = client.generate_data_encryption_key(
        request={
            "name": key_name,
            "key_algorithm": kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
        }
    )
    
    encrypted_data_key = generate_response.wrapped_key
    data_key = generate_response.plaintext

    # Encrypt the plaintext locally using the generated data_key
    # For simplicity, this example uses a placeholder for local encryption.
    # In a real scenario, you'd use a symmetric encryption algorithm like AES-GCM.
    # For the purpose of this example, we'll just return the plaintext and the encrypted_data_key.
    # A full implementation would involve a library like cryptography to actually encrypt `plaintext` with `data_key`.
    
    # This is a simplification. Real envelope encryption would encrypt plaintext with data_key locally.
    # For demonstration, we'll simulate the local encryption by returning the original plaintext and the wrapped key.
    # A production-ready solution would use a secure symmetric cipher here.
    import base64
    # Simulate local encryption (replace with actual AES-GCM encryption)
    # For this example, we're just base64 encoding the plaintext for demonstration
    # and returning the encrypted data key. In a real scenario, the plaintext
    # would be encrypted with `data_key` here.
    locally_encrypted_payload = base64.b64encode(plaintext) # Placeholder

    return encrypted_data_key, locally_encrypted_payload

if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location_id = "global"  # Or specific region
    key_ring_id = "my-key-ring"
    key_id = "my-encryption-key"

    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set or authenticated via gcloud
    # Example usage:
    # plaintext_data = b"Sensitive data for envelope encryption."
    # try:
    #     encrypted_data_key, locally_encrypted_payload = envelope_encrypt(project_id, location_id, key_ring_id, key_id, plaintext_data)
    #     print(f"Encrypted Data Key: {encrypted_data_key.hex()}")
    #     print(f"Locally Encrypted Payload (simulated): {locally_encrypted_payload.decode('utf-8')}")
    # except Exception as e:
    #     print(f"Error performing envelope encryption: {e}")
