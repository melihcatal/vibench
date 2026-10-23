from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import json
from typing import Dict, Any
from security_client import get_azure_vault_url


def parse_json_secret(secret_name: str) -> Dict[str, Any]:
    vault_url = get_azure_vault_url()
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    kv_secret = client.get_secret(secret_name)
    return json.loads(kv_secret.value)
