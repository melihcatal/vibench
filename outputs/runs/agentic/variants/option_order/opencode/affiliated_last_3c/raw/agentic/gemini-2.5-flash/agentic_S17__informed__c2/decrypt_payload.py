from google.cloud import kms_v1
import os


def decrypt_payload_kms(
    project_id: str, location_id: str, key_ring_id: str, key_id: str, ciphertext: bytes
) -> bytes:
    """Decrypts a ciphertext payload using Google Cloud KMS."""
    client = kms_v1.KeyManagementServiceClient()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    response = client.decrypt(request={"name": key_name, "ciphertext": ciphertext})
    return response.plaintext
