from google.cloud import kms_v1
import os


def encrypt_payload_kms(
    project_id: str, location_id: str, key_ring_id: str, key_id: str, plaintext: bytes
) -> bytes:
    """Encrypts a plaintext payload using Google Cloud KMS."""
    client = kms_v1.KeyManagementServiceClient()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    response = client.encrypt(request={"name": key_name, "plaintext": plaintext})
    return response.ciphertext
