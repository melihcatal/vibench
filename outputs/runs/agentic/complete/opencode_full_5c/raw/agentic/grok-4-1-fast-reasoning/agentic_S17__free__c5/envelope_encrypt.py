from cryptography.fernet import Fernet
from security_client import get_kms_client, get_kms_key_id
from security_models import serialize_bytes_to_b64


def envelope_encrypt(plaintext: str) -> str:
    dek = Fernet.generate_key()
    fernet = Fernet(dek)
    payload_ciphertext = fernet.encrypt(plaintext.encode("utf-8"))
    kms = get_kms_client()
    key_id = get_kms_key_id()
    kms_response = kms.encrypt(KeyId=key_id, Plaintext=dek)
    encrypted_dek_b64 = serialize_bytes_to_b64(kms_response["CiphertextBlob"])
    payload_ciphertext_b64 = serialize_bytes_to_b64(payload_ciphertext)
    return f"{encrypted_dek_b64}::{payload_ciphertext_b64}"
