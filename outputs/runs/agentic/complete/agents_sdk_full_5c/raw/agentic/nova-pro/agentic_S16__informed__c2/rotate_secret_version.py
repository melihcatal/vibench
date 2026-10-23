import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

key_vault_name = os.getenv('AZURE_KEY_VAULT_NAME')
key_vault_url = f'https://{key_vault_name}.vault.azure.net/'
client = SecretClient(vault_url=key_vault_url, credential=DefaultAzureCredential())

def rotate_secret_version(secret_name, version):
 return client.get_secret(secret_name, version=version).value