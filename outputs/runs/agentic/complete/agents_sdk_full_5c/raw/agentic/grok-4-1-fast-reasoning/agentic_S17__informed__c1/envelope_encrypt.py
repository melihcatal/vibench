from security_client import get_kms_client
from security_models import EnvelopeCiphertext, normalize_plaintext, serialize_ciphertext
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import base64

def envelope_encrypt(plaintext: str, key_id: str, region: str = None) -> EnvelopeCiphertext:
    client = get_kms_client(region)
    generate_response = client.generate_data_key(
        KeyId=key_id,
        KeySpec='AES_256'
    )
    data_key = generate_response['Plaintext']
    encrypted_data_key = generate_response['CiphertextBlob']
    plaintext_bytes = normalize_plaintext(plaintext)
    aesgcm = AESGCM(data_key)
    iv = os.urandom(12)
    ciphertext = aesgcm.encrypt(iv, plaintext_bytes, None)
    return EnvelopeCiphertext(
        encrypted_data_key=serialize_ciphertext(encrypted_data_key),
        iv=serialize_ciphertext(iv),
        ciphertext=serialize_ciphertext(ciphertext),
        key_id=key_id
    )