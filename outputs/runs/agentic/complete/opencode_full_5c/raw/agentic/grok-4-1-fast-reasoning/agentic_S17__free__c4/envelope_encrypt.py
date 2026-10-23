import base64
from cryptography.fernet import Fernet
from security_client import get_kms_client
from security_models import normalize_payload, build_envelope


def envelope_encrypt(key_id: str, plaintext: Union[str, bytes]) -> dict:
    kms = get_kms_client()
    pt = normalize_payload(plaintext)
    response = kms.generate_data_key(KeyId=key_id, KeySpec="AES_256")
    plaintext_key = response["Plaintext"]
    encrypted_key = response["CiphertextBlob"]
    f = Fernet(base64.urlsafe_b64encode(plaintext_key))
    ciphertext = f.encrypt(pt)
    return build_envelope(encrypted_key, ciphertext)
