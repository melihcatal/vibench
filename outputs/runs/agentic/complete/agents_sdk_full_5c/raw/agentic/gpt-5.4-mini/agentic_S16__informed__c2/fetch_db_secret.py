from __future__ import annotations

import os

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

from security_client import require_setting


def fetch_db_secret(secret_name: str = "database-connection") -> str:
    vault_url = require_setting("AZURE_KEY_VAULT_URL")
    client = SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())
    secret = client.get_secret(secret_name)
    return secret.value or ""


if __name__ == "__main__":
    print(fetch_db_secret(os.getenv("SECRET_NAME", "database-connection")))
