import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

key_vault_name = os.getenv('AZURE_KEY_VAULT_NAME')
key_vault_url = f'https://{key_vault_name}.vault.azure.net/'
client = SecretClient(vault_url=key_vault_url, credential=DefaultAzureCredential())

def fetch_db_secret(secret_name):
 return client.get_secret(secret_name).value