import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import json

credential = DefaultAzureCredential()
client = SecretClient(vault_url=os.getenv('AZURE_KEYVAULT_URL'), credential=credential)

def parse_json_secret(secret_name):
    secret_value = client.get_secret(secret_name).value
    return json.loads(secret_value)