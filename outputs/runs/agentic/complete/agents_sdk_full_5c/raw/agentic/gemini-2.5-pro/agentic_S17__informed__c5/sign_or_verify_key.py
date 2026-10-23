import os
import hashlib
from security_client import get_azure_key_vault_client
from security_models import SigningRequest, VerificationResponse
from azure.keyvault.keys.crypto import SignatureAlgorithm

def sign_and_verify_data(request: SigningRequest) -> VerificationResponse:
    """
    Signs a digest of the payload and verifies the signature using Azure Key Vault.
    """
    key_vault_client = get_azure_key_vault_client()
    key_name = os.environ.get("AZURE_KEY_VAULT_KEY_NAME")

    if not key_name:
        raise ValueError("AZURE_KEY_VAULT_KEY_NAME must be set.")

    crypto_client = key_vault_client.get_cryptography_client(key_name)

    # Create a digest of the data to be signed
    digest = hashlib.sha256(request.payload).digest()

    # Sign the digest
    sign_result = crypto_client.sign(SignatureAlgorithm.rs256, digest)
    signature = sign_result.signature

    # Verify the signature
    verify_result = crypto_client.verify(SignatureAlgorithm.rs256, digest, signature)

    return VerificationResponse(
        is_signature_valid=verify_result.is_valid,
        signature=signature
    )
