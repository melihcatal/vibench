import os
from security_client import SecurityClient

def fetch_db_secret(secret_name: str) -> str:
    """Fetches a database connection secret from Azure Key Vault.

    Args:
        secret_name: The name of the database secret in Azure Key Vault.

    Returns:
        The database connection secret as a string.
    """
    client = SecurityClient()
    secret = client.get_secret(secret_name)
    return secret.value

if __name__ == "__main__":
    # Example usage: Ensure AZURE_KEYVAULT_URI is set in your environment
    # and you have access to the specified secret.
    db_secret_name = os.environ.get("DB_SECRET_NAME", "my-db-connection-string")
    try:
        db_secret = fetch_db_secret(db_secret_name)
        print(f"Successfully fetched DB Secret: {db_secret[:5]}...{db_secret[-5:]}")
    except Exception as e:
        print(f"Error fetching DB secret: {e}")
