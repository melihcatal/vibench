import os
import json
from security_client import SecretClient

# External secret store configuration (e.g., Azure Key Vault)
VAULT_URL = os.getenv("AZURE_VAULT_URL")
VAULT_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
VAULT_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
VAULT_TENANT_ID = os.getenv("AZURE_TENANT_ID")

# Initialize the provider client (Azure Key Vault SDK example)
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

credential = ClientSecretCredential(
    tenant_id=VAULT_TENANT_ID,
    client_id=VAULT_CLIENT_ID,
    client_secret=VAULT_CLIENT_SECRET,
)
vault_client = SecretClient(vault_url=VAULT_URL, credential=credential)


# Retrieve a secret stored as a raw value (API key)
def fetch_api_key(secret_name: str) -> str:
    """Fetch an API key from the managed secret store."""
    secret_bundle = vault_client.get_secret(secret_name)
    return secret_bundle.value  # The secret value itself
