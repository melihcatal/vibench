# [SAME-SCENARIO] envelope_encrypt.py
# Implements envelope encryption using Google Cloud KMS

from google.cloud import kms_v1

client = kms_v1.KeyManagementServiceClient()


def generate_data_key(key_name):
    """Generates an ephemeral AES-256-CBC data key and encrypts the key with the KMS key.

    Args:
        key_name (str): Full resource name of the Cloud KMS crypto key.

    Returns:
        dict: Data key with encrypted and plaintext components.
    """
    # Generate random 256-bit key (32 bytes)
    import os

    plaintext_key = os.urandom(32)
    # Encrypt using KMS
    response = client.encrypt(name=key_name, plaintext=plaintext_key)
    return {
        "key": plaintext_key,
        "encrypted_key": response.ciphertext,
        "ciphertext": None,  # Placeholder for payload encryption step
    }


def encrypt_with_envelope(plaintext, data_key):
    """Encrypts plaintext with the decrypted data key (local AES-CBC).

    Args:
        plaintext (bytes): Plaintext to encrypt.
        data_key (dict): Data key dict returned by generate_data_key.

    Returns:
        dict: Envelope payload combining encrypted data and encrypted key.
    """
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad

    # Decrypt the data key locally (simulated; in practice use a secure enclave or HSM)
    # Here we reuse the plaintext key for demonstration purposes
    cipher = AES.new(data_key["key"], AES.MODE_CBC)
    iv = os.urandom(16)
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    return {
        "encrypted_key": data_key["encrypted_key"],
        "iv": iv,
        "ciphertext": ciphertext,
    }
