import base64
import os

from security_client import kms_client, load_config


def envelope_encrypt(payload: str, key_id: str | None = None) -> dict:
    config = load_config()
    client = kms_client(config)
    data_key = client.generate_data_key(
        KeyId=key_id or config.key_id, KeySpec="AES_256"
    )
    plaintext_key = data_key["Plaintext"]
    encrypted_key = base64.b64encode(data_key["CiphertextBlob"]).decode("utf-8")
    iv = os.urandom(12)
    ciphertext = bytes(
        a ^ b
        for a, b in zip(
            payload.encode("utf-8"),
            plaintext_key * ((len(payload) // len(plaintext_key)) + 1),
        )
    )
    return {
        "key_id": key_id or config.key_id,
        "encrypted_data_key": encrypted_key,
        "iv": base64.b64encode(iv).decode("utf-8"),
        "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
    }
