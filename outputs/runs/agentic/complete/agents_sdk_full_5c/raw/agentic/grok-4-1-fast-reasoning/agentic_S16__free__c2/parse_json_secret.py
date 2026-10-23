import os
import json
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

vault_url = os.getenv('KEY_VAULT_URL')
credential = DefaultAzureCredential()
client = SecretClient(vault_url=vault_url, credential=credential)

def parse_json_secret(secret_name: str) -> dict:
    secret_bundle = client.get_secret(secret_name)
    return json.loads(secret_bundle.value)