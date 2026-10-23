from google.cloud import kms_v1

def decrypt_payload_with_kms(project_id: str, location_id: str, key_ring_id: str, key_id: str, ciphertext: bytes) -> bytes:
    """
    Decrypts a ciphertext payload with a Google Cloud KMS managed key.
    """
    client = kms_v1.KeyManagementServiceClient()
    key_name = client.key_path(project_id, location_id, key_ring_id, key_id)

    # Decrypt the ciphertext
    response = client.decrypt(request={"name": key_name, "ciphertext": ciphertext})
    return response.plaintext
