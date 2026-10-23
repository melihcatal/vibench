from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

def fetch_db_secret(secret_name: str) -> str:
    """
    Fetches a database connection secret from Azure Key Vault.
    Requires AZURE_KEY_VAULT_URL environment variable.
    """
    key_vault_url = os.environ.get("AZURE_KEY_VAULT_URL")
    if not key_vault_url:
        raise ValueError("AZURE_KEY_VAULT_URL environment variable not set.")

    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_url, credential=credential)

    try:
        secret = client.get_secret(secret_name)
        return secret.value
    except Exception as e:
        print(f"Error fetching secret '{secret_name}' from Azure Key Vault: {e}")
        raise

if __name__ == '__main__':
    # Example usage (requires AZURE_KEY_VAULT_URL set and Azure login)
    # os.environ['AZURE_KEY_VAULT_URL'] = 'https://<your-key-vault-name>.vault.azure.net'
    # os.environ['DB_SECRET_NAME'] = 'your-db-connection-string-secret'
    secret_name = os.environ.get('DB_SECRET_NAME', 'your-db-secret-name')
    try:
        db_secret = fetch_db_secret(secret_name)
        print(f"Successfully fetched DB secret (first 5 chars): {db_secret[:5]}*****")
    except Exception:
        print("Failed to fetch DB secret.")
