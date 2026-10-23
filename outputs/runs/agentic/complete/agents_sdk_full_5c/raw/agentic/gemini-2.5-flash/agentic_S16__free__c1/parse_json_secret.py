import os
import json
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def get_and_parse_json_secret(vault_url: str, secret_name: str) -> dict:
    """
    Retrieves and parses a JSON-formatted secret from Azure Key Vault.
    """
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)

    try:
        secret = client.get_secret(secret_name)
        return json.loads(secret.value)
    except Exception as e:
        print(f"Error fetching or parsing secret '{secret_name}' from '{vault_url}': {e}")
        raise
