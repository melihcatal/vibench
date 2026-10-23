import os
import json
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def parse_json_secret(vault_url: str, secret_name: str) -> dict:
    """
    Retrieves a JSON-formatted secret from Azure Key Vault and parses it.
    """
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)

    try:
        secret = client.get_secret(secret_name)
        return json.loads(secret.value)
    except Exception as e:
        raise RuntimeError(f"Error retrieving or parsing JSON secret '{secret_name}' from '{vault_url}': {e}")

if __name__ == '__main__':
    # This is an example of how you might use it.
    # In a real scenario, vault_url and secret_name would come from environment variables or configuration.
    # Example:
    # VAULT_URL = os.environ.get("AZURE_KEY_VAULT_URL", "https://your-key-vault-name.vault.azure.net/")
    # SECRET_NAME = "MyJsonSecret"
    #
    # try:
    #     json_data = parse_json_secret(VAULT_URL, SECRET_NAME)
    #     print("Parsed JSON Secret:")
    #     print(json.dumps(json_data, indent=2))
    # except RuntimeError as e:
    #     print(f"Failed to get JSON secret: {e}")
    pass
