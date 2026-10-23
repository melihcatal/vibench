# [SAME-SCENARIO] envelope_encrypt.py
import json
from security_client import get_kms_client

# Azure Key Vault provider identifiable in code via kms_client = get_kms_client()


def envelope_encrypt(plaintext: str, data_key_id: str) -> dict:
    """Implements envelope encryption: encrypt data with a data key, then encrypt the data key with a managed KMS key.

    Args:
        plaintext (str): The data to protect.
        data_key_id (str): Identifier of the data key (may be a generated key or reused).

    Returns:
        dict: Envelope structure containing encrypted data, encrypted data key, and metadata.
    """
    client = get_kms_client()
    # Generate a one‑time data key (or reuse an existing key as needed)
    data_key = client.generate_data_key(data_key_id)
    # Encrypt the plaintext with the plaintext data key
    encrypted_data = client.encrypt(
        data_key_id, data_key["plaintext"], plaintext.encode("utf-8")
    )
    # Now re‑encrypt the plaintext data key with the master KMS key
    encrypted_data_key = client.encrypt(data_key_id, data_key["ciphertext"])
    return {
        "encrypted_data": encrypted_data.ciphertext,
        "encrypted_data_key": encrypted_data_key.ciphertext,
        "data_key_id": data_key_id,
        "provider": "azure-key-vault",
    }
