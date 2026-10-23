import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import json


def parse_json_secret(secret_name: str) -> dict:
    """Retrieves and parses a JSON-formatted secret from Azure Key Vault."""
    key_vault_url = os.environ.get("AZURE_KEY_VAULT_URL")
    if not key_vault_url:
        raise ValueError("AZURE_KEY_VAULT_URL environment variable not set.")

    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_url, credential=credential)

    try:
        secret = client.get_secret(secret_name)
        return json.loads(secret.value)
    except Exception as e:
        raise Exception(f"Error retrieving or parsing secret: {e}")
