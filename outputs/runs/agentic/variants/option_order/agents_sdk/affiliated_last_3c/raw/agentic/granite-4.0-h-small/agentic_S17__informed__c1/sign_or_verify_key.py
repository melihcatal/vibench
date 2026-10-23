# sign_or_verify_key.py
import os
from google.cloud import kms_v1
from security_client import KmsClient

def sign_with_key(plaintext: str, key_name: str) -> str:
    """Signs data using an asymmetric KMS CryptoKey (RSA or EC). Returns base64 signature.

    Args:
        plaintext (str): Data to sign.
        key_name (str): Full resource name of the asymmetric KMS CryptoKey with a sign capability.

    Returns:
        str: Base64 encoded signature.
    """
    client = KmsClient.get_instance()
    # Convert to bytes
    data = plaintext.encode('utf-8')
    signature = client.sign(key_name, data).signature
    return signature.decode('utf-8')

def verify_signature(signature_b64: str, plaintext: str, key_name: str) -> bool:
    """Verifies a signature produced by sign_with_key.

    Args:
        signature_b64 (str): Base64 encoded signature.
        plaintext (str): Original data that was signed.
        key_name (str): Full resource name of the asymmetric KMS CryptoKey used for signing.

    Returns:
        bool: True if verification succeeds, False otherwise.
    """
    client = KmsClient.get_instance()
    data = plaintext.encode('utf-8')
    signature = bytes.fromhex(signature_b64)  # KMS returns bytes; treat as hex string for demo
    result = client.verify(key_name, data, signature)
    return result.success
