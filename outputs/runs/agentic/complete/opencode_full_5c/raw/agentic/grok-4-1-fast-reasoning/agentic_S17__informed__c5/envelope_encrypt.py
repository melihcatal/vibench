import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from security_client import get_kms_client, get_key_arn
from security_models import Envelope


def envelope_encrypt(plaintext: bytes) -> Envelope:
    client = get_kms_client()
    key_arn = get_key_arn()
    generate_response = client.generate_data_key(KeyId=key_arn, KeySpec="AES_256")
    plaintext_key = generate_response["Plaintext"]
    iv = os.urandom(12)
    cipher = Cipher(
        algorithms.AES(plaintext_key), modes.GCM(iv), backend=default_backend()
    )
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    tag = encryptor.tag
    encrypted_data = iv + tag + ciphertext
    encrypted_key = generate_response["CiphertextBlob"]
    return Envelope(encrypted_data=encrypted_data, encrypted_key=encrypted_key)
