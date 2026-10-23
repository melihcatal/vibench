from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import json
from typing import Dict, Any

from security_client import get_secrets_config

def parse_json_secret(secret_name: str) -> dict:
    config = get_secrets_config()
    vault_url = config['azure_vault_url']
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    secret_bundle = client.get_secret(secret_name)
    return json.loads(secret_bundle.value)