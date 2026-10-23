import os
from cryptography.fernet import Fernet
from security_client import get_kms_client


def envelope_encrypt(plaintext: bytes, key_id: str = None) -> dict:
    client = get_kms_client()
    key_id = key_id or os.getenv("AWS_KMS_KEY_ID")
    if not key_id:
        raise ValueError("AWS_KMS_KEY_ID required")
    data_key_response = client.generate_data_key(KeyId=key_id, KeySpec="AES_256")
    data_key = data_key_response["Plaintext"]
    encrypted_data_key = data_key_response["CiphertextBlob"]
    fernet = Fernet(data_key)
    ciphertext = fernet.encrypt(plaintext)
    return {"encrypted_data_key": encrypted_data_key, "ciphertext": ciphertext}
