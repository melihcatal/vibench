from security_client import AzureKeyVaultSecurityClient
from security_models import SecretInfo
import os

def rotate_secret_version(secret_name: str, new_secret_value: str, vault_url: str = None) -> SecretInfo:
    client = AzureKeyVaultSecurityClient(vault_url)
    # In a real rotation, you would typically generate a new secret value externally
    # and then set it. For this example, we're taking `new_secret_value` directly.
    updated_secret = client.set_secret(secret_name, new_secret_value)
    return updated_secret

def read_secret_version(secret_name: str, version: str, vault_url: str = None) -> SecretInfo:
    client = AzureKeyVaultSecurityClient(vault_url)
    secret = client.get_secret_version(secret_name, version)
    return secret
