from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import os
import json
from security_models import SecretRequest, SecretResponse

def parse_json_secret(req: SecretRequest) -> dict:
    vault_url = os.getenv("AZURE_KEY_VAULT_URL")
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    secret = client.get_secret(req.name)
    value = json.loads(secret.value)
    return value