import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from security_client import get_kms_client, normalize_key_id
from security_models import EnvelopeBundle, encode_bytes


def envelope_encrypt(plaintext: str, key_id: str | None = None) -> EnvelopeBundle:
    kms = get_kms_client()
    key = normalize_key_id(key_id)
    data_key = kms.generate_data_key(KeyId=key, KeySpec="AES_256")
    raw_key = data_key["Plaintext"]
    wrapped_key = data_key["CiphertextBlob"]
    iv = os.urandom(12)
    aesgcm = AESGCM(raw_key)
    ciphertext = aesgcm.encrypt(iv, plaintext.encode("utf-8"), None)
    return EnvelopeBundle(
        wrapped_key=encode_bytes(wrapped_key),
        data_key=encode_bytes(raw_key),
        iv=encode_bytes(iv),
        ciphertext=encode_bytes(ciphertext),
        key_id=key,
    )
