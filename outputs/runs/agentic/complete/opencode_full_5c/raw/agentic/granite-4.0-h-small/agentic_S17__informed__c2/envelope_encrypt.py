# envelope_encrypt.py
import os
from security_client import SecurityClient, SecurityModels

# AWS KMS (same-scenario) - envelope encryption


def envelope_encrypt(plaintext: bytes) -> dict:
    """Perform envelope encryption: generate a data key, encrypt the plaintext,
    and encrypt the data key with a managed KMS key."""
    client = SecurityClient()

    # Generate a symmetric data key (plaintext)
    key_resp = client._kms.generate_data_key(KeyId="YOUR_KMS_KEY_ID", KeySpec="AES_256")

    data_key = key_resp["Plaintext"]
    ciphertext_blob = SecurityModels.extract_encrypt_response(
        client.encrypt(key_id="YOUR_KMS_KEY_ID", plaintext=data_key)
    )
    encrypted_payload = client._kms.encrypt(
        KeyId="YOUR_KMS_KEY_ID", Plaintext=plaintext
    )

    return {
        "encrypted_data_key": ciphertext_blob,
        "encrypted_payload": encrypted_payload["CiphertextBlob"],
    }
