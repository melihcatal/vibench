import os
import hashlib
from azure.keyvault.keys.crypto import CryptographyClient, SignatureAlgorithm

from security_client import get_azure_key_vault_crypto_client
from security_models import SigningRequest, VerificationRequest


def sign_digest_azure(request: SigningRequest) -> bytes:
    """
    Signs a pre-calculated digest using an Azure Key Vault key.
    """
    crypto_client: CryptographyClient = get_azure_key_vault_crypto_client()

    # The data to sign must be a pre-calculated digest.
    hasher = hashlib.sha256()
    hasher.update(request.data)
    digest = hasher.digest()

    sign_result = crypto_client.sign(SignatureAlgorithm.rs256, digest)
    return sign_result.signature


def verify_signature_azure(request: VerificationRequest) -> bool:
    """
    Verifies a signature against a pre-calculated digest using an Azure Key Vault key.
    """
    crypto_client: CryptographyClient = get_azure_key_vault_crypto_client()

    # The data to verify must also be a pre-calculated digest.
    hasher = hashlib.sha256()
    hasher.update(request.data)
    digest = hasher.digest()

    verify_result = crypto_client.verify(
        SignatureAlgorithm.rs256, digest, request.signature
    )
    return verify_result.is_valid
