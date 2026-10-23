import json
from security_client import SecretClient

# Use Azure Key Vault as the managed store (example)
VAULT_URL = os.getenv("AZURE_VAULT_URL")
VAULT_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
VAULT_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
VAULT_TENANT_ID = os.getenv("AZURE_TENANT_ID")

from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

credential = ClientSecretCredential(
    tenant_id=VAULT_TENANT_ID,
    client_id=VAULT_CLIENT_ID,
    client_secret=VAULT_CLIENT_SECRET,
)
vault_client = SecretClient(vault_url=VAULT_URL, credential=credential)


# Read a specific secret version (or staged value)
def rotate_secret_version(secret_name: str, version: int | str = None) -> str:
    """Get a particular version of a secret or the latest staged value."""
    if version:
        # Azure secrets are immutable; you retrieve a specific version directly
        secret_bundle = vault_client.get_secret_version(secret_name, version=version)
    else:
        # Defaults to latest staged version if applicable
        secret_bundle = vault_client.get_secret(secret_name)
    return secret_bundle.value
