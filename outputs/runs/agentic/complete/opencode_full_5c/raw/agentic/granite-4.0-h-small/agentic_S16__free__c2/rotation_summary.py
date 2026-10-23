# rotation_summary.py
# [LATER-STEP] Summarize secret rotation status (using Azure Key Vault metadata)

from security_client import get_secret_manager_client
from typing import Dict, Any


def rotate_summary(secret_name: str) -> Dict[str, Any]:
    """Return a concise summary of secret versions and staging labels.

    Args:
        secret_name: Identifier of the secret in Azure Key Vault.

    Returns:
        Dict containing current, previous, and pending versions.
    """
    client = get_secret_manager_client(provider="azure")
    secret_bundle = client.get_secret(name=secret_name)
    # Azure returns 'attributes' with 'enabled', 'created', 'updated', 'recoveryLevel'
    # and a list of 'tags' that can include version labels if set via SetSecret
    summary = {
        "name": secret_name,
        "current_version": secret_bundle.properties.version,
        "enabled": secret_bundle.properties.enabled,
        "tags": secret_bundle.properties.tags,
    }
    return summary
