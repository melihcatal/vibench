import os
import json
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def parse_json_secret(key_vault_name: str, secret_name: str) -> dict:
    """
    Retrieves and parses a JSON-formatted secret from Azure Key Vault.
    """
    key_vault_uri = f"https://{key_vault_name}.vault.azure.net"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_uri, credential=credential)

    try:
        secret = client.get_secret(secret_name)
        return json.loads(secret.value)
    except Exception as e:
        raise Exception(f"Failed to retrieve or parse secret {secret_name} from {key_vault_name}: {e}")

if __name__ == "__main__":
    # Example usage:
    # Set AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET or use Azure CLI login
    # vault_name = os.environ.get("AZURE_KEY_VAULT_NAME", "your-key-vault-name")
    # secret = "my-json-config"
    # json_data = parse_json_secret(vault_name, secret)
    # print(f"Parsed JSON Secret: {json_data}")
    pass
