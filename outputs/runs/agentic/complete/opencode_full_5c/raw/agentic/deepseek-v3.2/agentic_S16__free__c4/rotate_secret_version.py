import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def rotate_secret_version(
    key_vault_name: str, secret_name: str, version: str = None
) -> str:
    """Read a specific secret version or staged value from Azure Key Vault."""
    key_vault_url = f"https://{key_vault_name}.vault.azure.net"

    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_url, credential=credential)

    try:
        if version:
            secret = client.get_secret(secret_name, version=version)
        else:
            secret = client.get_secret(secret_name)

        if secret.value:
            return secret.value
        else:
            raise ValueError(f"Secret {secret_name} has no value")

    except Exception as e:
        if "SecretNotFound" in str(e):
            raise ValueError(
                f"Secret {secret_name} not found in Azure Key Vault {key_vault_name}"
            )
        elif "Forbidden" in str(e) or "Access denied" in str(e):
            raise PermissionError(f"Access denied to Azure Key Vault {key_vault_name}")
        elif "Invalid version" in str(e):
            raise ValueError(f"Invalid version {version} for secret {secret_name}")
        else:
            raise RuntimeError(f"Error accessing Azure Key Vault: {e}")
