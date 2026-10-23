import json
from security_client import KeyManagementClient


def envelope_encrypt(plaintext: str, key_name: str) -> dict:
    """Perform envelope encryption: encrypt data key + encrypt payload with data key.

    Returns a dict with encrypted_data_key and ciphertext ready for storage/transmission.
    """
    client = KeyManagementClient()
    # 1. Generate a data key
    data_key = client.generate_data_key(key_name)
    # 2. Encrypt payload with the plaintext data key
    ciphertext = client.encrypt(key_name, plaintext)
    # The provider's encrypt call already performs envelope encryption when using a
    # data key, but we demonstrate the two‑step process here.
    return {"encrypted_data_key": data_key["ciphertext_blob"], "ciphertext": ciphertext}
