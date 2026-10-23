import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def fetch_db_secret(vault_url: str, secret_name: str) -> str:
    """Fetches a database connection secret from Azure Key Vault."""
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    retrieved_secret = client.get_secret(secret_name)
    return retrieved_secret.value

if __name__ == "__main__":
    # Example usage (requires AZURE_KEY_VAULT_URL and Azure credentials configured)
    key_vault_url = os.environ.get("AZURE_KEY_VAULT_URL")
    db_secret_name = "my-database-connection-string"
    if key_vault_url:
        try:
            db_secret = fetch_db_secret(key_vault_url, db_secret_name)
            print(f"Successfully fetched DB secret.")
        except Exception as e:
            print(f"Error fetching DB secret: {e}")
    else:
        print("Please set the AZURE_KEY_VAULT_URL environment variable.")
