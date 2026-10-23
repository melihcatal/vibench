from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from typing import Dict, Any
from security_client import get_azure_config
from security_models import parse_json_secret, build_db_connection, DBConnectionSecret

def fetch_db_secret(secret_name: str) -> DBConnectionSecret:
    config = get_azure_config()
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=config['vault_url'], credential=credential)
    secret_bundle = client.get_secret(secret_name)
    secret_str = secret_bundle.value
    secret_parsed = parse_json_secret(secret_str)
    return build_db_connection(secret_parsed)
