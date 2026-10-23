import os
from security_client import AzureKeyVaultSecurityClient
from security_models import EnvelopeEncryptionRequest

def envelope_encrypt(plaintext: str) -> dict:
    key_vault_url = os.environ.get("KEY_VAULT_URL")
    key_name = os.environ.get("KEY_NAME")

    if not key_vault_url or not key_name:
        raise ValueError("KEY_VAULT_URL and KEY_NAME environment variables must be set.")

    client = AzureKeyVaultSecurityClient(key_vault_url=key_vault_url)
    request = EnvelopeEncryptionRequest(plaintext=plaintext, key_name=key_name, key_vault_url=key_vault_url)
    response = client.envelope_encrypt(request)
    
    return {
        "ciphertext": response.ciphertext,
        "wrapped_key": response.wrapped_key,
        "key_id": response.key_id,
        "algorithm": response.algorithm
    }

