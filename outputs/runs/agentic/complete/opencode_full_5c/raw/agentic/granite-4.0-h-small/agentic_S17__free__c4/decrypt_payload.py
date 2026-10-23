import base64, json
from security_client import get_key_management_client

# Azure Key Vault integration – uses Azure Key Vault for decryption


def decrypt_payload(ciphertext_b64: str, key_id: str) -> str:
    """Decrypt a base64‑encoded ciphertext using a managed key.

    Returns the original plaintext string.
    """
    client = get_key_management_client()
    ciphertext = base64.b64decode(ciphertext_b64)
    # Azure Key Vault decrypt API
    response = client.decrypt(key=key_id, ciphertext=ciphertext)
    plaintext = response["Plaintext"].decode("utf-8")
    return plaintext
