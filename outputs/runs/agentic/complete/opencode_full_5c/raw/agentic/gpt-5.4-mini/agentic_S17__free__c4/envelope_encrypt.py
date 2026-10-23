import base64
from cryptography.fernet import Fernet
from security_client import SecurityClient


def envelope_encrypt(payload: str) -> dict:
    client = SecurityClient()
    data_key = Fernet.generate_key()
    data_cipher = Fernet(data_key)
    ciphertext = data_cipher.encrypt(payload.encode("utf-8"))
    wrapped = client.encrypt(base64.urlsafe_b64encode(data_key).decode("ascii"))
    return {
        "key_id": wrapped["key_id"],
        "encrypted_key": wrapped["ciphertext"],
        "ciphertext": base64.urlsafe_b64encode(ciphertext).decode("ascii"),
    }
