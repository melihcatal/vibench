import os
import hashlib
from azure.keyvault.keys.crypto import SignatureAlgorithm
from security_client import get_azure_crypto_client

def sign_and_verify_with_azure(message: bytes, key_name: str) -> bool:
    """
    Signs a message digest and verifies the signature using Azure Key Vault.
    """
    # Provider-specific integration with Azure Key Vault
    crypto_client = get_azure_crypto_client(key_name)
    
    # Create a digest of the message
    digest = hashlib.sha256(message).digest()
    
    # Sign the digest
    sign_result = crypto_client.sign(SignatureAlgorithm.rs256, digest)
    signature = sign_result.signature
    
    # Verify the signature
    verify_result = crypto_client.verify(SignatureAlgorithm.rs256, digest, signature)
    
    return verify_result.is_valid
