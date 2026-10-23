from azure.keyvault.keys import KeyClient
from azure.identity import DefaultAzureCredential

key_vault_name = "your-key-vault-name"

def get_key_client() -> KeyClient:
    credential = DefaultAzureCredential()
    key_client = KeyClient(vault_url=f"https://{key_vault_name}.vault.azure.net/", credential=credential)
    return key_client