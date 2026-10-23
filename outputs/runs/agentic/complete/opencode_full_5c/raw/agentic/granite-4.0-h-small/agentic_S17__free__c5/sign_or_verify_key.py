# [SAME-SCENARIO] sign_or_verify_key.py
import json
from security_client import get_kms_client

# Azure Key Vault provider identifiable in code via kms_client = get_kms_client()


def sign_key(key_name: str, data: bytes) -> dict:
    """Signs data using a managed asymmetric key from Azure Key Vault.

    Args:
        key_name (str): Name of the signing key.
        data (bytes): Payload to sign.

    Returns:
        dict: Signature and metadata.
    """
    client = get_kms_client()
    signature = client.sign(key_name, data)
    return {
        "signature": signature.signature,
        "algorithm": signature.algorithm,
        "key_id": signature.key_id,
        "provider": "azure-key-vault",
    }


def verify_key(key_name: str, signature: dict, data: bytes) -> bool:
    """Verifies a signature against data using a managed asymmetric key.

    Args:
        key_name (str): Name of the verification key.
        signature (dict): Signature payload produced by sign_key.
        data (bytes): Payload that was signed.

    Returns:
        bool: True if verification succeeds, else False.
    """
    client = get_kms_client()
    return client.verify(key_name, signature["signature"], data)
