import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Initialize the client
credential = DefaultAzureCredential()
key_vault_name = os.getenv('AZURE_KEY_VAULT_NAME')
key_vault_url = f'https://{key_vault_name}.vault.azure.net/'
client = SecretClient(vault_url=key_vault_url, credential=credential)

# Fetch a specific secret version
secret_name = 'specific-secret'
secret_version = '1'
secret = client.get_secret(secret_name, secret_version)
print(f'Specific Secret Version: {secret.value}')