import base64
import os

from security_client import create_kms_client, get_kms_key_id
from security_models import EnvelopeCiphertext


def envelope_encrypt(plaintext, key_id=None):
    kms = create_kms_client()
    target_key_id = key_id or get_kms_key_id()
    data_key = kms.generate_data_key(KeyId=target_key_id, KeySpec="AES_256")
    iv = os.urandom(12)
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    except Exception as exc:
        raise RuntimeError("cryptography package is required for AWS envelope encryption") from exc
    aesgcm = AESGCM(data_key["Plaintext"])
    ciphertext = aesgcm.encrypt(iv, plaintext.encode("utf-8") if isinstance(plaintext, str) else plaintext, None)
    return EnvelopeCiphertext(
        encrypted_data_key=base64.b64encode(data_key["CiphertextBlob"]).decode("utf-8"),
        iv=base64.b64encode(iv).decode("utf-8"),
        ciphertext=base64.b64encode(ciphertext).decode("utf-8"),
        key_id=data_key["KeyId"],
    ).to_payload()
