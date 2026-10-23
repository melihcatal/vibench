from azure.keyvault.keys import KeyClient
from azure.identity import DefaultAzureCredential

def get_key_client():
    credential = DefaultAzureCredential()
    client = KeyClient(vault_url="https://<your-key-vault-name>.vault.azure.net/", credential=credential)
    return client