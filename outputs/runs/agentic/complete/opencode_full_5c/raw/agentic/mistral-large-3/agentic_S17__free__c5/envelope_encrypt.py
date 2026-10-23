import os
import json
from cryptography.fernet import Fernet
from security_client import SecurityClient
from security_models import (
    EncryptionRequest,
    DecryptionRequest,
    normalize_payload,
    serialize_response,
)


def envelope_encrypt(plaintext: str, context: dict = None) -> str:
    client = SecurityClient()
    request = EncryptionRequest(plaintext=plaintext, context=context)
    normalized = normalize_payload(request.dict())

    key_data = client.generate_data_key()
    fernet_key = client.generate_fernet_key(key_data["plaintext_key"])
    fernet = Fernet(fernet_key.encode())

    ciphertext = fernet.encrypt(normalized["plaintext"])

    response = {
        "ciphertext": ciphertext.decode(),
        "encrypted_key": key_data["encrypted_key"],
        "key_id": os.getenv("GOOGLE_KMS_KEY_NAME"),
        "algorithm": "AES256_GCM_ENVELOPE",
    }
    return serialize_response(response)


def envelope_decrypt(ciphertext: str, encrypted_key: str, context: dict = None) -> str:
    client = SecurityClient()
    request = DecryptionRequest(
        ciphertext=ciphertext, encrypted_key=encrypted_key, context=context
    )
    normalized = normalize_payload(request.dict())

    plaintext_key = client.decrypt_symmetric(normalized["encrypted_key"])
    fernet_key = client.generate_fernet_key(plaintext_key)
    fernet = Fernet(fernet_key.encode())

    plaintext = fernet.decrypt(normalized["ciphertext"])

    response = {
        "plaintext": plaintext.decode(),
        "key_id": os.getenv("GOOGLE_KMS_KEY_NAME"),
        "algorithm": "AES256_GCM_ENVELOPE",
    }
    return serialize_response(response)
