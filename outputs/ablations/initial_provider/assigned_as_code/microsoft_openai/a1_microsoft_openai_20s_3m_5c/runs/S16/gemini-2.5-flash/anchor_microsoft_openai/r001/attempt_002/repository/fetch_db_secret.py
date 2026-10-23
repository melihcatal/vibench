from security_client import AzureKeyVaultSecurityClient
from security_models import SecretInfo
import os

def fetch_db_secret(secret_name: str, vault_url: str = None) -> SecretInfo:
    client = AzureKeyVaultSecurityClient(vault_url)
    db_secret = client.get_secret(secret_name)
    return db_secret
