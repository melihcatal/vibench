import os
import json
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

key_vault_name = os.getenv('AZURE_KEY_VAULT_NAME')
key_vault_url = f'https://{key_vault_name}.vault.azure.net/'

credential = DefaultAzureCredential()
client = SecretClient(vault_url=key_vault_url, credential=credential)

secret_name = 'json-secret'
secret = client.get_secret(secret_name)
json_secret = json.loads(secret.value)
print(json_secret)