from google.cloud.kms_v1.types import EncryptRequest, DecryptRequest

def normalize_encrypt_request(project_id, location_id, key_ring_id, crypto_key_id, plaintext):
    return EncryptRequest(name=f"projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{crypto_key_id}", plaintext=plaintext)

def normalize_decrypt_request(project_id, location_id, key_ring_id, crypto_key_id, ciphertext):
    return DecryptRequest(name=f"projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{crypto_key_id}", ciphertext=ciphertext)