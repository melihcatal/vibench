import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def get_secret_client():
 key_vault_name = os.getenv('AZURE_KEY_VAULT_NAME')
 key_vault_url = f'https://{key_vault_name}.vault.azure.net/'
 return SecretClient(vault_url=key_vault_url, credential=DefaultAzureCredential())