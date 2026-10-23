import os
import json
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def parse_json_secret(vault_url: str, secret_name: str) -> dict:
    """Retrieves and parses a JSON-formatted secret from Azure Key Vault."""
    # DefaultAzureCredential tries various auth methods, including environment variables like AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_CLIENT_SECRET
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)

    try:
        secret = client.get_secret(secret_name)
        if secret.value:
            return json.loads(secret.value)
        else:
            raise ValueError(f"Secret '{secret_name}' from Azure Key Vault has no value.")
    except Exception as e:
        raise ValueError(f"Error retrieving or parsing secret '{secret_name}' from Key Vault '{vault_url}': {e}") from e
