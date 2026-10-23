import os
from typing import Any, Dict, Optional

from security_client import get_secret_manager_client, get_secret_name
from security_models import SecretFetchRequest, parse_json_or_string_secret

# Azure Key Vault integration
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def parse_json_secret(vault_url: Optional[str] = None, secret_name: Optional[str] = None, version: Optional[str] = None) -> Dict[str, Any]:
    url = vault_url or os.getenv("AZURE_KEY_VAULT_URL")
    name = secret_name or os.getenv("JSON_SECRET_NAME", "config-json")
    client = get_secret_manager_client(provider="azure", vault_url=url)
    request = SecretFetchRequest(secret_name=get_secret_name(None, name), version=version or "")
    secret_bundle = client.get_secret(request.secret_name, version=request.version or None)
    return parse_json_or_string_secret(secret_bundle.value)
