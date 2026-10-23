from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import json

def parse_json_secret():
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url="https://<your-key-vault-name>.vault.azure.net/", credential=credential)
    secret_name = "example-json-secret"
    retrieved_secret = client.get_secret(secret_name)
    return json.loads(retrieved_secret.value)