import os
from azure.keyvault.keys import KeyClient
from azure.identity import DefaultAzureCredential

key_vault_name = os.getenv('AZURE_KEY_VAULT_NAME')
key_client = KeyClient(vault_url=f'https://{key_vault_name}.vault.azure.net/', credential=DefaultAzureCredential())

def get_key_client():
    return key_client
