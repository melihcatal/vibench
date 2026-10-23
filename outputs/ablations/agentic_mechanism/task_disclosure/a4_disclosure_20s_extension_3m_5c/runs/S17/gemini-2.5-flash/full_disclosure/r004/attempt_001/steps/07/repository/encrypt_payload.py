from google.cloud import kms_v1

def encrypt_payload(project_id: str, location_id: str, key_ring_id: str, key_id: str, plaintext: bytes) -> bytes:
    """
    Encrypts a plaintext payload with a managed key using Google Cloud KMS.
    """
    client = kms_v1.KeyManagementServiceClient()
    name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)
    response = client.encrypt(name=name, plaintext=plaintext)
    return response.ciphertext
