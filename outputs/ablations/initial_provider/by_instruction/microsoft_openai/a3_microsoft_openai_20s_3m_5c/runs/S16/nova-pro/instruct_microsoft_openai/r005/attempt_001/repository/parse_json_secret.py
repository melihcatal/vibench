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

# Fetch the JSON-formatted secret
secret_name = 'json-secret'
json_secret = client.get_secret(secret_name).value

import json
parsed_secret = json.loads(json_secret)

print(f'Parsed JSON Secret: {parsed_secret}')
