# sign_or_verify_key.py
import hashlib
from azure.keyvault.keys.crypto import SignatureAlgorithm
from security_client import get_azure_key_client
from security_models import SignPayload, VerifyPayload

def sign_with_azure(payload: SignPayload) -> bytes:
    """
    Signs a digest using a key in Azure Key Vault.
    """
    key_client = get_azure_key_client()
    crypto_client = key_client.get_cryptography_client(payload.key_name, payload.key_version)

    # Note: Azure Key Vault signs a digest, not the raw data.
    hasher = hashlib.sha256()
    hasher.update(payload.data_to_sign)
    digest = hasher.digest()

    result = crypto_client.sign(SignatureAlgorithm.RS256, digest)
    return result.signature


def verify_with_azure(payload: VerifyPayload) -> bool:
    """
    Verifies a signature using a key in Azure Key Vault.
    """
    key_client = get_azure_key_client()
    crypto_client = key_client.get_cryptography_client(payload.key_name, payload.key_version)

    hasher = hashlib.sha256()
    hasher.update(payload.data_to_verify)
    digest = hasher.digest()
    
    result = crypto_client.verify(SignatureAlgorithm.RS256, digest, payload.signature)
    return result.is_valid
