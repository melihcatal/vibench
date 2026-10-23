import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Azure Key Vault configuration
key_vault_name = os.getenv('AZURE_KEY_VAULT_NAME')
key_vault_url = f'https://{key_vault_name}.vault.azure.net/'

# Authenticate using DefaultAzureCredential
credential = DefaultAzureCredential()

# Create a SecretClient
client = SecretClient(vault_url=key_vault_url, credential=credential)

# Fetch the API key
secret_name = 'api-key'
api_key = client.get_secret(secret_name).value

print(f'API Key: {api_key}')
