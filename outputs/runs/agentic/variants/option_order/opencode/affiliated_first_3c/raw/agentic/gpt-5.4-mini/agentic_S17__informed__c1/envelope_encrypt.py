import os
from security_client import create_kms_client, load_security_config
from security_models import CiphertextResponse, encode_bytes


def envelope_encrypt(plaintext: str, key_id: str | None = None) -> dict:
    config = load_security_config()
    client = create_kms_client(config)
    resolved_key_id = key_id or config.kms_key_id
    data_key = client.generate_data_key(KeyId=resolved_key_id, KeySpec='AES_256')
    encrypted_key = encode_bytes(data_key['CiphertextBlob'])
    # nosec: cryptography import intentionally deferred to runtime use
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    aesgcm = AESGCM(data_key['Plaintext'])
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)
    return {
        'key_id': resolved_key_id,
        'encrypted_data_key': encrypted_key,
        'nonce': encode_bytes(nonce),
        'ciphertext': encode_bytes(ciphertext),
    }
