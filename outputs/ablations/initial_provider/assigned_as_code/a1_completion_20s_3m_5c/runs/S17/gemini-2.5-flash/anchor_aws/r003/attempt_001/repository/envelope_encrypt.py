import boto3
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def envelope_encrypt(payload, config=None):
    config = config or {}
    client = boto3.client("kms", region_name=config.get("region"))

    # 1. Generate a data key from KMS
    response = client.generate_data_key(
        KeyId=config["key_id"],
        KeySpec="AES_256"
    )
    plaintext_data_key = response["Plaintext"]
    encrypted_data_key = response["CiphertextBlob"]

    # 2. Use the plaintext data key to encrypt the payload locally
    iv = os.urandom(16) # Initialization vector
    cipher = Cipher(algorithms.AES(plaintext_data_key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(payload["plaintext"]) + encryptor.finalize()
    tag = encryptor.tag

    # 3. Return the ciphertext, the encrypted data key, and IV/tag
    return {
        "ciphertext": ciphertext,
        "encrypted_data_key": encrypted_data_key,
        "iv": iv,
        "tag": tag
    }