from cryptography.fernet import Fernet
from security_client import get_kms_client
from security_models import normalize_payload

def envelope_encrypt(payload: bytes, key_id: str) -> tuple[bytes, bytes]:
    dek = Fernet.generate_key()
    f = Fernet(dek)
    encrypted_payload = f.encrypt(payload)
    kms = get_kms_client()
    encrypted_dek_response = kms.encrypt(
        KeyId=key_id,
        Plaintext=dek
    )
    encrypted_dek = encrypted_dek_response['CiphertextBlob']
    return encrypted_payload, encrypted_dek

def envelope_encrypt_str(payload: str, key_id: str) -> tuple[bytes, bytes]:
    norm_payload = normalize_payload(payload)
    return envelope_encrypt(norm_payload, key_id)