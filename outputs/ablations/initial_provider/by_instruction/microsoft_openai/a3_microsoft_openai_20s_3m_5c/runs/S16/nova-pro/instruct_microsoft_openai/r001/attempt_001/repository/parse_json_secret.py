import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import json

# Initialize the client
credential = DefaultAzureCredential()
key_vault_name = os.getenv('AZURE_KEY_VAULT_NAME')
key_vault_url = f'https://{key_vault_name}.vault.azure.net/'
client = SecretClient(vault_url=key_vault_url, credential=credential)

# Fetch the JSON-formatted secret
secret_name = 'json-secret'
secret = client.get_secret(secret_name)
parsed_secret = json.loads(secret.value)
print(f'Parsed JSON Secret: {parsed_secret}')