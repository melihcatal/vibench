import os
import json
from typing import Any, Dict, Optional

from azure.keyvault.secrets import SecretClient
from security_client import get_azure_key_vault_secret_client
from security_models import Secret

def parse_json_secret(vault_url: str, secret_name: str) -> Optional[Dict[str, Any]]:
    client: SecretClient = get_azure_key_vault_secret_client(vault_url)
    try:
        key_vault_secret = client.get_secret(secret_name)
        if key_vault_secret.value:
            return json.loads(key_vault_secret.value)
    except Exception as e:
        print(f"Error fetching or parsing JSON secret '{secret_name}' from Azure Key Vault: {e}")
    return None

if __name__ == '__main__':
    # Example usage (requires AZURE_VAULT_URL and appropriate Azure credentials)
    # For demonstration, assume a secret 'my-json-config' exists in Azure Key Vault
    # and contains a JSON string, e.g., '{"key":"value"}'.
    vault_url = os.environ.get("AZURE_VAULT_URL")
    if not vault_url:
        print("Please set the AZURE_VAULT_URL environment variable.")
    else:
        json_secret_content = parse_json_secret(vault_url, os.environ.get("JSON_SECRET_NAME", "my-json-config"))
        if json_secret_content:
            print(f"Fetched and parsed JSON Secret: {json.dumps(json_secret_content, indent=2)}")
        else:
            print("Failed to fetch or parse JSON Secret.")
