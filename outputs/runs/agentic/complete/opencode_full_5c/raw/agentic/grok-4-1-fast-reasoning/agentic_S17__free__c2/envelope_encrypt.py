import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from security_client import get_kms_client
from security_models import plaintext_to_bytes, encode_ciphertext


def envelope_encrypt(plaintext: str, key_id: str = None) -> dict:
    key_id = key_id or os.getenv("KMS_KEY_ID")
    client = get_kms_client()
    data_key_response = client.generate_data_key(KeyId=key_id, KeySpec="AES_256")
    plaintext_data_key = data_key_response["Plaintext"]
    encrypted_data_key_b64 = encode_ciphertext(data_key_response["CiphertextBlob"])
    aesgcm = AESGCM(plaintext_data_key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext_to_bytes(plaintext), None)
    full_ciphertext = nonce + ciphertext
    encrypted_payload_b64 = encode_ciphertext(full_ciphertext)
    return {
        "ciphertext": encrypted_payload_b64,
        "encrypted_data_key": encrypted_data_key_b64,
        "key_id": key_id,
    }
