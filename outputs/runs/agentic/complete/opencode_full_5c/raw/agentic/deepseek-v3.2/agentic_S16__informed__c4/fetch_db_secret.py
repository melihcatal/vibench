import os
import json
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential


def fetch_db_secret(secret_name: str, vault_url: str = None) -> dict:
    """Fetch a database connection secret from Azure Key Vault."""
    if vault_url is None:
        vault_url = os.environ.get("AZURE_KEY_VAULT_URL")
        if not vault_url:
            raise ValueError(
                "Azure Key Vault URL must be provided or set in AZURE_KEY_VAULT_URL environment variable"
            )

    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)

    secret = client.get_secret(secret_name)
    db_config = json.loads(secret.value)

    return db_config
