import os
from security_client import AzureKeyVaultSecurityClient
from security_models import EncryptionRequest

def encrypt_payload(plaintext: str) -> dict:
    key_vault_url = os.environ.get("KEY_VAULT_URL")
    key_name = os.environ.get("KEY_NAME")

    if not key_vault_url or not key_name:
        raise ValueError("KEY_VAULT_URL and KEY_NAME environment variables must be set.")

    client = AzureKeyVaultSecurityClient(key_vault_url=key_vault_url)
    request = EncryptionRequest(plaintext=plaintext, key_name=key_name, key_vault_url=key_vault_url)
    response = client.encrypt(request)
    
    return {
        "ciphertext": response.ciphertext,
        "key_id": response.key_id,
        "algorithm": response.algorithm
    }

