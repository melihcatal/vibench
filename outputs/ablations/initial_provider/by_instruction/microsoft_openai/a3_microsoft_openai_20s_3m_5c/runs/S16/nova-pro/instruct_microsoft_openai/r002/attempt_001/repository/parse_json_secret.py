import json
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def parse_json_secret():
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url="https://<your-key-vault-name>.vault.azure.net/", credential=credential)
    json_secret = client.get_secret("json-secret").value
    return json.loads(json_secret)