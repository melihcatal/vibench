# [SAME-SCENARIO] rotate_secret_version.py
import os
from security_client import SecretManagerClient

def rotate_secret_version(secret_name, version_id):
    """Read a specific version (or staged value) of a secret from HashiCorp Vault.

    Args:
        secret_name (str): Path to the secret in Vault (e.g. secret/data/myapp).
        version_id (str): Version identifier or 'staged' to get the staged value.

    Returns:
        dict: Data from the requested secret version.
    """
    client = SecretManagerClient(provider='hashicorp')
    response = client.read_secret_version(secret_name, version_id)
    # Response is already JSON‑decoded by the client helper
    return response
