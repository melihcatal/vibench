from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import json
from typing import Dict, Any
from security_client import get_provider_config
from security_models import DbSecret, SecretMetadata


def fetch_db_secret(secret_name: str) -> DbSecret:
    config = get_provider_config("azure")
    vault_url = config["vault_url"]
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    secret_bundle = client.get_secret(secret_name)
    metadata: SecretMetadata = {
        "name": secret_bundle.name,
        "version_id": secret_bundle.version,
        "created_time": str(secret_bundle.properties.created_on)
        if secret_bundle.properties.created_on
        else None,
    }
    secret_value = secret_bundle.value
    db_data: Dict[str, Any] = json.loads(secret_value)
    return {
        "metadata": metadata,
        "connection_string": db_data.get("connection_string", ""),
        "username": db_data.get("username", ""),
        "password": db_data.get("password", ""),
        "host": db_data.get("host", ""),
        "port": db_data.get("port"),
    }
