from security_client import SecurityClient
from security_models import SignVerifyRequest, SignResponse, VerifyResponse
import base64
from hashlib import sha256

def sign_data(request: SignVerifyRequest) -> SignResponse:
    """Signs data with a managed key using Azure Key Vault."""
    security_client = SecurityClient(request.key_vault_url)
    crypto_client = security_client.get_cryptography_client(request.key_name)

    # Hash the data before signing
    hashed_data = sha256(request.data.encode('utf-8')).digest()

    # Sign the hash using the specified key in Azure Key Vault
    sign_result = crypto_client.sign(request.algorithm, hashed_data)

    return SignResponse(
        signature=base64.b64encode(sign_result.signature).decode('utf-8'),
        key_id=sign_result.key_id
    )

def verify_signature(request: SignVerifyRequest, signature: str) -> VerifyResponse:
    """Verifies a signature with a managed key using Azure Key Vault."""
    security_client = SecurityClient(request.key_vault_url)
    crypto_client = security_client.get_cryptography_client(request.key_name)

    # Hash the data before verification (must be the same hashing algorithm as used for signing)
    hashed_data = sha256(request.data.encode('utf-8')).digest()

    # Convert base64 signature back to bytes
    signature_bytes = base64.b64decode(signature)

    # Verify the signature using the specified key in Azure Key Vault
    is_valid = crypto_client.verify(request.algorithm, hashed_data, signature_bytes)

    return VerifyResponse(
        is_valid=is_valid
    )

