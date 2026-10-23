import base64
import os

from security_client import get_kms_client
from security_models import normalize_text, response_dict


def envelope_encrypt(plaintext: str, key_id: str):
    client = get_kms_client()
    data_key = client.generate_data_key(KeyId=normalize_text(key_id), KeySpec="AES_256")
    dek_plaintext = data_key["Plaintext"]
    dek_ciphertext = data_key["CiphertextBlob"]
    iv = os.urandom(12)
    cipher = __import__(
        "cryptography.hazmat.primitives.ciphers.aead", fromlist=["AESGCM"]
    ).AESGCM(dek_plaintext)
    ciphertext = cipher.encrypt(iv, normalize_text(plaintext).encode("utf-8"), None)
    return response_dict(
        key_id=normalize_text(key_id),
        encrypted_data_key=base64.b64encode(dek_ciphertext).decode("ascii"),
        iv=base64.b64encode(iv).decode("ascii"),
        ciphertext=base64.b64encode(ciphertext).decode("ascii"),
        provider="aws-kms",
    )
