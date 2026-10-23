import os
from security_client import AzureKeyVaultSecurityClient
from security_models import DecryptionRequest

def decrypt_payload(ciphertext: str, key_id: str, algorithm: str) -> dict:
    key_vault_url = os.environ.get("KEY_VAULT_URL")
    
    if not key_vault_url:
        raise ValueError("KEY_VAULT_URL environment variable must be set.")

    client = AzureKeyVaultSecurityClient(key_vault_url=key_vault_url)
    request = DecryptionRequest(ciphertext=ciphertext, key_id=key_id, algorithm=algorithm)
    response = client.decrypt(request)
    
    return {
        "plaintext": response.plaintext
    }

