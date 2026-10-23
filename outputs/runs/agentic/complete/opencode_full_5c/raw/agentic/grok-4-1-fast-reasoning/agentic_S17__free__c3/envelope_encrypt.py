import boto3
import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def envelope_encrypt(plaintext: bytes, key_id: str = None) -> dict:
    if key_id is None:
        key_id = os.getenv("AWS_KMS_KEY_ID")
    kms = boto3.client("kms", region_name="us-east-1")
    data_key_response = kms.generate_data_key(KeyId=key_id, KeySpec="AES_256_GCM")
    data_key = data_key_response["Plaintext"]
    encrypted_data_key = data_key_response["CiphertextBlob"]
    nonce = os.urandom(12)
    aesgcm = AESGCM(data_key)
    ciphertext = aesgcm.encrypt(nonce=nonce, data=plaintext, associated_data=b"")
    return {
        "encrypted_data_key": base64.b64encode(encrypted_data_key).decode("utf-8"),
        "nonce": base64.b64encode(nonce).decode("utf-8"),
        "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
    }
