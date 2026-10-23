# [SAME-SCENARIO] fetch_api_key.py
# Retrieve an API key from a managed secrets store using HashiCorp Vault SDK

import os
from hashicorp.vault import Vault

VAULT_ADDR = os.getenv("VAULT_ADDR")
VAULT_TOKEN = os.getenv("VAULT_TOKEN")


def fetch_api_key(secret_path: str) -> str:
    """Fetches an API key stored at secret_path in Vault.

    Args:
        secret_path: Path where the API key is stored in Vault.

    Returns:
        The API key string.
    """
    vault = Vault(address=VAULT_ADDR, token=VAULT_TOKEN)
    response = vault.read(secret_path)
    # Assume the secret contains a field called "api_key"
    return response["data"]["api_key"]
