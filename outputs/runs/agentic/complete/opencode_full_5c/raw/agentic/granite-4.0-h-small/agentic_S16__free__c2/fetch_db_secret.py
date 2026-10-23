# fetch_db_secret.py
# [SAME-SCENARIO] Fetch a database connection secret (Azure Key Vault secret)

import os
from security_client import get_secret_manager_client


def fetch_db_secret(secret_name: str) -> dict:
    """
    Retrieve a database connection secret containing user, password, host, and dbname.

    Args:
        secret_name: Name of the secret in Azure Key Vault.

    Returns:
        Dictionary with keys: user, password, host, dbname.
    """
    client = get_secret_manager_client()
    secret_bundle = client.get_secret(name=secret_name)
    return secret_bundle.value  # assumes secret value is a JSON string
