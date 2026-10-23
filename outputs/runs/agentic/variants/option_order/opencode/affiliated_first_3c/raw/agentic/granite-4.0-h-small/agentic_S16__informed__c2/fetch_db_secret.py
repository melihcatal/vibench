import os
import json

# Provider-specific configuration
# Using Azure Key Vault Secrets
AZURE_VAULT_URL = os.getenv("AZURE_KEY_VAULT_URL")
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")

from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

credential = ClientSecretCredential(
    tenant_id=AZURE_TENANT_ID,
    client_id=AZURE_CLIENT_ID,
    client_secret=AZURE_CLIENT_SECRET,
)
client = SecretClient(vault_url=AZURE_VAULT_URL, credential=credential)


def fetch_db_secret(secret_name: str) -> dict:
    """Fetch a database connection secret from Azure Key Vault.
    Returns the secret value as a dict.
    """
    retrieved = client.get_secret(secret_name)
    # Azure returns the secret value in the 'value' field
    return json.loads(retrieved.value)


if __name__ == "__main__":
    secret_name = os.getenv("DB_SECRET_NAME")
    if secret_name:
        secret = fetch_db_secret(secret_name)
        print("Fetched secret:", secret)
    else:
        print("Set DB_SECRET_NAME env var")
