from google.cloud import kms_v1
import os


def envelope_encrypt_kms(
    project_id: str, location_id: str, key_ring_id: str, key_id: str, plaintext: bytes
) -> tuple[bytes, bytes]:
    """Implements envelope encryption using Google Cloud KMS."""
    client = kms_v1.KeyManagementServiceClient()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Generate a new data encryption key and encrypt it with the KMS key
    generate_dek_response = client.generate_random_bytes(
        request={
            "project_id": project_id,
            "location_id": location_id,
            "length_bytes": 32,
        }  # 256-bit key
    )
    dek = generate_dek_response.data

    # Encrypt the DEK with KMS
    encrypt_dek_response = client.encrypt(request={"name": key_name, "plaintext": dek})
    encrypted_dek = encrypt_dek_response.ciphertext

    # For demonstration, we'll use a simple XOR cipher with the DEK to encrypt the actual payload
    # In a real-world scenario, you would use a robust symmetric encryption algorithm (e.g., AES)
    encrypted_payload = bytes(
        [p ^ d for p, d in zip(plaintext, dek * (len(plaintext) // len(dek) + 1))]
    )

    return encrypted_payload, encrypted_dek
