from __future__ import annotations

import os

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

from security_client import load_secret_name, require_setting


def fetch_api_key(secret_name: str | None = None) -> str:
    vault_url = require_setting("AZURE_KEY_VAULT_URL")
    client = SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())
    key_name = secret_name or load_secret_name("api-key")
    return client.get_secret(key_name).value or ""


if __name__ == "__main__":
    print(fetch_api_key(os.getenv("SECRET_NAME")))
