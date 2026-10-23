import json
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def parse_json_secret(vault_url, secret_name):
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    secret = client.get_secret(secret_name)
    return json.loads(secret.value)