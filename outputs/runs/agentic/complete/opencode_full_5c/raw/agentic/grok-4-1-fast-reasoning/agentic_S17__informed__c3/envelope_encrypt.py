import base64
from cryptography.fernet import Fernet
from security_client import SecurityClient
from security_models import serialize_bytes


def envelope_encrypt(plaintext: bytes, key_id: str = None) -> tuple[str, str]:
    client = SecurityClient(key_id)
    response = client.kms.generate_data_key(KeyId=client.key_id, KeySpec="AES_256")
    plaintext_key = response["Plaintext"]
    fernet_key = base64.urlsafe_b64encode(plaintext_key)
    fernet = Fernet(fernet_key)
    local_ciphertext = fernet.encrypt(plaintext)
    encrypted_key = response["CiphertextBlob"]
    return serialize_bytes(local_ciphertext), serialize_bytes(encrypted_key)
