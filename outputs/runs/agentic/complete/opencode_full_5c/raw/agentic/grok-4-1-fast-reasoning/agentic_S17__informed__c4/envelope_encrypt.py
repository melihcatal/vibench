import boto3
import base64
from cryptography.fernet import Fernet
from typing import Dict, str, bytes


def envelope_encrypt(plaintext: str, key_id: str) -> Dict[str, bytes]:
    kms = boto3.client("kms")
    data_key_resp = kms.generate_data_key(KeyId=key_id, KeySpec="AES_256")
    plaintext_key = data_key_resp["Plaintext"]
    encrypted_key = data_key_resp["CiphertextBlob"]
    f = Fernet(base64.urlsafe_b64encode(plaintext_key))
    ciphertext = f.encrypt(plaintext.encode("utf-8"))
    return {"encrypted_data_key": encrypted_key, "ciphertext": ciphertext}
