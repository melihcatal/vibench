import os
import json
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from security_models import ParsedSecret

def get_and_parse_json_secret(vault_url: str, secret_name: str) -> ParsedSecret | None:
    """
    Retrieves a secret from Azure Key Vault and parses it as JSON.

    Args:
        vault_url: The URL of the Azure Key Vault.
        secret_name: The name of the secret to retrieve.

    Returns:
        A ParsedSecret object, or None if retrieval or parsing fails.
    """
    try:
        # Using DefaultAzureCredential for authentication
        # It tries multiple authentication methods (e.g., env vars, managed identity)
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=vault_url, credential=credential)

        retrieved_secret = client.get_secret(secret_name)
        secret_value = retrieved_secret.value

        if not secret_value:
            print(f"Secret '{secret_name}' is empty.")
            return None

        secret_data = json.loads(secret_value)
        return ParsedSecret(name=secret_name, data=secret_data)

    except json.JSONDecodeError:
        print(f"Failed to parse JSON from secret '{secret_name}'.")
        return None
    except Exception as e:
        print(f"An error occurred while fetching secret '{secret_name}': {e}")
        return None

# Example usage would be in a different file.
# if __name__ == "__main__":
#     key_vault_name = os.environ.get("AZURE_KEY_VAULT_NAME")
#     json_secret_name = os.environ.get("JSON_SECRET_NAME")

#     if key_vault_name and json_secret_name:
#         kv_uri = f"https://{key_vault_name}.vault.azure.net"
#         parsed_secret = get_and_parse_json_secret(kv_uri, json_secret_name)
#         if parsed_secret:
#             print(f"Successfully retrieved and parsed secret: {parsed_secret.name}")
#             print(f"Data keys: {list(parsed_secret.data.keys())}")
#         else:
#             print("Failed to process secret.")
#     else:
#         print("Please set AZURE_KEY_VAULT_NAME and JSON_SECRET_NAME environment variables.")
