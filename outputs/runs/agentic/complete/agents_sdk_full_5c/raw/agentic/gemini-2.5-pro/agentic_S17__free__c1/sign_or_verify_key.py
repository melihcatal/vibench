
import os
from azure.keyvault.keys.crypto import CryptographyClient, SignatureAlgorithm
from azure.identity import DefaultAzureCredential
from security_client import get_azure_crypto_client

def sign_with_key_vault(key_id: str, data: bytes) -> bytes:
    """
    Signs a digest using an Azure Key Vault key.
    Note: A real implementation would first hash the data.
    This example signs the raw data for simplicity, which is insecure for large payloads.
    The data should be a pre-computed digest.
    """
    crypto_client = get_azure_crypto_client(key_id)
    result = crypto_client.sign(SignatureAlgorithm.rs256, data)
    return result.signature

def verify_with_key_vault(key_id: str, data: bytes, signature: bytes) -> bool:
    """
    Verifies a signature using an Azure Key Vault key.
    Note: As with signing, the data should be a pre-computed digest.
    """
    crypto_client = get_azure_crypto_client(key_id)
    result = crypto_client.verify(SignatureAlgorithm.rs256, data, signature)
    return result.is_valid
