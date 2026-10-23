from azure.keyvault.keys import KeyClient
from azure.identity import DefaultAzureCredential

def get_key_vault_key_client(key_vault_url: str) -> KeyClient:
    """
    Provides a configured Azure Key Vault KeyClient.
    """
    credential = DefaultAzureCredential()
    key_client = KeyClient(vault_url=key_vault_url, credential=credential)
    return key_client
