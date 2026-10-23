import os
from security_client import AzureKeyVaultSecurityClient
from security_models import SignRequest, VerifyRequest

def sign_payload(digest: bytes, algorithm: str) -> dict:
    key_vault_url = os.environ.get("KEY_VAULT_URL")
    key_name = os.environ.get("KEY_NAME")

    if not key_vault_url or not key_name:
        raise ValueError("KEY_VAULT_URL and KEY_NAME environment variables must be set.")

    client = AzureKeyVaultSecurityClient(key_vault_url=key_vault_url)
    request = SignRequest(digest=digest, key_name=key_name, key_vault_url=key_vault_url, algorithm=algorithm)
    response = client.sign(request)
    
    return {
        "signature": response.signature.hex(),
        "key_id": response.key_id
    }

def verify_payload(digest: bytes, signature: bytes, key_id: str, algorithm: str) -> dict:
    key_vault_url = os.environ.get("KEY_VAULT_URL")
    key_name = os.environ.get("KEY_NAME") # Key name might not be strictly needed for verify if key_id is sufficient, but good to have consistency

    if not key_vault_url or not key_name:
        raise ValueError("KEY_VAULT_URL and KEY_NAME environment variables must be set.")

    # Extract key_name from key_id for consistency with the client's _get_cryptography_client method
    # This is a simplification; a more robust solution might parse the key_id properly or pass key_id directly
    # For now, assuming key_id contains the full key path and the client can handle it.
    # The client's _get_cryptography_client already takes the full key_id. So key_name is not strictly needed here
    # if key_id is fully qualified. Let's adjust to pass key_id directly.

    client = AzureKeyVaultSecurityClient(key_vault_url=key_vault_url)
    request = VerifyRequest(
        digest=digest,
        signature=signature,
        key_name=key_name, # This will be used to construct the full key_id in the client, even if key_id is passed fully qualified
        key_vault_url=key_vault_url,
        algorithm=algorithm
    )
    response = client.verify(request)
    
    return {
        "is_valid": response.is_valid
    }
