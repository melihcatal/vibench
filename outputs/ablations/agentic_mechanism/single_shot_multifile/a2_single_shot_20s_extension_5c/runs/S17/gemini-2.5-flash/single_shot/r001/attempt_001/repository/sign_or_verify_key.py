from security_client import SecurityClients
from security_models import SignRequest, SignResponse, VerifyRequest, VerifyResponse
from azure.keyvault.keys.crypto import CryptographyClient
from azure.keyvault.keys.models import JsonWebKey, KeyOperation, KeyType
from azure.core.exceptions import ResourceNotFoundError

def sign_with_key_vault(request: SignRequest) -> SignResponse:
    key_vault_client = SecurityClients.get_azure_key_vault_client()
    
    # Key ID in Azure Key Vault is the key name.
    try:
        key = key_vault_client.get_key(request.key_id)
    except ResourceNotFoundError:
        raise ValueError(f"Key '{request.key_id}' not found in Azure Key Vault.")

    crypto_client = CryptographyClient(key, key_vault_client.credential)

    # Determine algorithm mapping for Azure Key Vault
    # Example: PS256 -> PS256, RS256 -> RS256
    azure_algorithm = request.algorithm

    sign_result = crypto_client.sign(azure_algorithm, request.digest)

    return SignResponse(
        key_id=request.key_id,
        signature=sign_result.signature
    )

def verify_with_key_vault(request: VerifyRequest) -> VerifyResponse:
    key_vault_client = SecurityClients.get_azure_key_vault_client()
    
    try:
        key = key_vault_client.get_key(request.key_id)
    except ResourceNotFoundError:
        raise ValueError(f"Key '{request.key_id}' not found in Azure Key Vault.")

    crypto_client = CryptographyClient(key, key_vault_client.credential)

    azure_algorithm = request.algorithm

    verify_result = crypto_client.verify(azure_algorithm, request.digest, request.signature)

    return VerifyResponse(
        key_id=request.key_id,
        is_valid=verify_result.is_valid
    )