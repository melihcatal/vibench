import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Initialize the client
credential = DefaultAzureCredential()
key_vault_name = os.getenv('AZURE_KEY_VAULT_NAME')
key_vault_url = f'https://{key_vault_name}.vault.azure.net/'
client = SecretClient(vault_url=key_vault_url, credential=credential)

# Fetch the API key
secret_name = 'api-key'
secret = client.get_secret(secret_name)
print(f'API Key: {secret.value}')