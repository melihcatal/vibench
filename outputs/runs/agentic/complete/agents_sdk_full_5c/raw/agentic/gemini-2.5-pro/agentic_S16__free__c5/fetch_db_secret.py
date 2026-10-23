
import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def get_database_secret(vault_url: str, secret_name: str) -> str | None:
    """
    Fetches a database connection secret from Azure Key Vault.

    Args:
        vault_url: The URL of the Azure Key Vault.
        secret_name: The name of the secret to fetch.

    Returns:
        The secret value, or None if an error occurs.
    """
    try:
        # Use DefaultAzureCredential which supports various authentication methods
        # like environment variables, managed identity, etc.
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=vault_url, credential=credential)

        retrieved_secret = client.get_secret(secret_name)
        return retrieved_secret.value
    except Exception as e:
        print(f"Error fetching secret from Azure Key Vault: {e}")
        return None

if __name__ == '__main__':
    # Example usage:
    # Set environment variables for authentication, e.g.,
    # AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_CLIENT_SECRET
    KEY_VAULT_URL = os.environ.get("AZURE_KEY_VAULT_URL")
    DB_SECRET_NAME = os.environ.get("AZURE_DB_SECRET_NAME", "database-connection-string")

    if not KEY_VAULT_URL:
        print("AZURE_KEY_VAULT_URL environment variable not set.")
    else:
        db_connection_string = get_database_secret(KEY_VAULT_URL, DB_SECRET_NAME)
        if db_connection_string:
            print("Successfully fetched database secret.")
            # Be careful printing secrets in a real application
            # print(f"Connection String: {db_connection_string}")
        else:
            print("Failed to fetch database secret.")
