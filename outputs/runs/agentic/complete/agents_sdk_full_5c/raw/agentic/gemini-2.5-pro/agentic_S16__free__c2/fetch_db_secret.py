import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from security_models import DatabaseCredentials

def get_akv_client(vault_url: str) -> SecretClient:
    """Creates a client for Azure Key Vault."""
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    return client

def fetch_db_secret(secret_name: str) -> DatabaseCredentials | None:
    """
    Fetches a database connection secret from Azure Key Vault.

    Args:
        secret_name: The name of the secret to fetch.

    Returns:
        A DatabaseCredentials object or None if an error occurs.
    """
    key_vault_name = os.environ.get("AZURE_KEY_VAULT_NAME")
    if not key_vault_name:
        print("AZURE_KEY_VAULT_NAME environment variable not set.")
        return None

    vault_url = f"https://{key_vault_name}.vault.azure.net/"
    
    try:
        client = get_akv_client(vault_url)
        retrieved_secret = client.get_secret(secret_name)
        
        # Assuming the secret value is a connection string like "user:password"
        user, password = retrieved_secret.value.split(":", 1)
        
        creds = DatabaseCredentials(
            username=user,
            password=password,
            engine="postgresql", 
            host="db.example.com",
            port=5432,
            dbname="production"
        )
        return creds

    except Exception as e:
        print(f"Failed to retrieve secret '{secret_name}' from Azure Key Vault: {e}")
        return None

