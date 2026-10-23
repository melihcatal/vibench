import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient

def get_key_vault_url():
    key_vault_url = os.environ.get("AZURE_KEY_VAULT_URL")
    if not key_vault_url:
        raise ValueError("AZURE_KEY_VAULT_URL environment variable not set.")
    return key_vault_url

def get_cryptography_client(key_id: str) -> CryptographyClient:
    credential = DefaultAzureCredential()
    # The CryptographyClient expects the key_id to be the full URL to the key, e.g., https://<vault-name>.vault.azure.net/keys/<key-name>/<key-version>
    # So, we pass the key_id directly as the vault_url.
    return CryptographyClient(key_id, credential=credential)
