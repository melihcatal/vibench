from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient
from azure.keyvault.keys import KeyClient

def get_key_vault_crypto_client(key_id: str) -> CryptographyClient:
    """Returns an authenticated CryptographyClient for Azure Key Vault."""
    credential = DefaultAzureCredential()
    return CryptographyClient(key_id, credential=credential)

def get_key_vault_key_client(key_vault_url: str) -> KeyClient:
    """Returns an authenticated KeyClient for Azure Key Vault."""
    credential = DefaultAzureCredential()
    return KeyClient(key_vault_url, credential=credential)
