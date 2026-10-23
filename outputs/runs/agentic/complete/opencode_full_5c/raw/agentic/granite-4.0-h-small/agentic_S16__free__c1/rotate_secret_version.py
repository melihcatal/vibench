# [SAME-SCENARIO] rotate_secret_version.py
# Read a specific secret version or staged value from Azure Key Vault

import os
from azure.keyvault.secrets import SecretClient

VAULT_URL = os.getenv("AZURE_KEYVAULT_URL")

client = SecretClient(
    vault_url=VAULT_URL, credential=None
)  # Assuming managed identity or env auth


def rotate_secret_version(secret_name: str, version_id: str):
    """Read a specific version or staged value of a secret from Azure Key Vault.

    Args:
        secret_name: Name of the secret.
        version_id: Specific version ID or "staged" to get pending rotation.

    Returns:
        The secret value as a string.
    """
    try:
        secret_bundle = client.get_secret(secret_name=secret_name, version=version_id)
        return secret_bundle.value
    except Exception as e:
        raise RuntimeError(
            f"Failed to rotate secret {secret_name} version {version_id}: {e}"
        )
