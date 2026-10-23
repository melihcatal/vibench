import os
import hashlib
from azure.keyvault.keys.crypto import SignatureAlgorithm
from security_client import get_azure_crypto_client
from security_models import SigningRequest, VerificationRequest, SigningResponse, VerificationResponse

def sign_with_azure_key_vault(request: SigningRequest) -> SigningResponse:
    """
    Signs a data digest using a key from Azure Key Vault.
    """
    key_vault_uri = os.environ.get("AZURE_KEY_VAULT_URI")
    if not key_vault_uri:
        return SigningResponse(signature=b"", key_id=request.key_id, algorithm=request.algorithm, success=False, error="AZURE_KEY_VAULT_URI not set.")

    crypto_client = get_azure_crypto_client(key_vault_uri)
    key_id_with_version = f"{request.key_id}/versions/{request.key_version}"

    digest = hashlib.sha256(request.data_to_sign).digest()

    try:
        result = crypto_client.sign(
            key_id=key_id_with_version,
            algorithm=SignatureAlgorithm[request.algorithm],
            digest=digest
        )
        return SigningResponse(
            signature=result.signature,
            key_id=result.key_id,
            algorithm=request.algorithm,
            success=True
        )
    except Exception as e:
        return SigningResponse(signature=b"", key_id=request.key_id, algorithm=request.algorithm, success=False, error=str(e))


def verify_with_azure_key_vault(request: VerificationRequest) -> VerificationResponse:
    """
    Verifies a signature using a key from Azure Key Vault.
    """
    key_vault_uri = os.environ.get("AZURE_KEY_VAULT_URI")
    if not key_vault_uri:
        return VerificationResponse(is_valid=False, key_id=request.key_id, algorithm=request.algorithm, success=False, error="AZURE_KEY_VAULT_URI not set.")

    crypto_client = get_azure_crypto_client(key_vault_uri)
    key_id_with_version = f"{request.key_id}/versions/{request.key_version}"

    digest = hashlib.sha256(request.data_to_verify).digest()

    try:
        result = crypto_client.verify(
            key_id=key_id_with_version,
            algorithm=SignatureAlgorithm[request.algorithm],
            digest=digest,
            signature=request.signature
        )
        return VerificationResponse(
            is_valid=result.is_valid,
            key_id=result.key_id,
            algorithm=request.algorithm,
            success=True
        )
    except Exception as e:
        return VerificationResponse(is_valid=False, key_id=request.key_id, algorithm=request.algorithm, success=False, error=str(e))
