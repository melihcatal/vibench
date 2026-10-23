import json
import os
from typing import Optional
from security_client import get_azure_key_vault_client
from security_models import DatabaseCredentials

def fetch_database_secret_from_azure(secret_name: str) -> Optional[DatabaseCredentials]:
    """
    Fetches a database connection secret from Azure Key Vault.
    Assumes the secret is stored as a JSON string with connection details.

    Args:
        secret_name: The name of the secret in Azure Key Vault.

    Returns:
        A DatabaseCredentials object or None if the secret is not found.
    """
    try:
        vault_url = os.environ["AZURE_KEY_VAULT_URL"]
        client = get_azure_key_vault_client(vault_url)
        retrieved_secret = client.get_secret(secret_name)
    except (KeyError, Exception):
        return None

    if retrieved_secret.value:
        secret_data = json.loads(retrieved_secret.value)
        return DatabaseCredentials(
            username=secret_data.get("username"),
            password=secret_data.get("password"),
            host=secret_data.get("host"),
            port=secret_data.get("port"),
            dbname=secret_data.get("dbname"),
        )
    return None
