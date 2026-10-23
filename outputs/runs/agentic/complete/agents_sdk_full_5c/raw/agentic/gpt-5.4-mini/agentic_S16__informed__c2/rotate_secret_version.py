from __future__ import annotations

import os

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

from security_client import require_setting


def rotate_secret_version(secret_name: str, version_id: str | None = None, stage: str | None = None) -> str:
    vault_url = require_setting("AZURE_KEY_VAULT_URL")
    client = SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())
    if version_id:
        return client.get_secret(secret_name, version_id=version_id).value or ""
    if stage:
        return client.get_secret(secret_name, version_id=stage).value or ""
    return client.get_secret(secret_name).value or ""


if __name__ == "__main__":
    print(rotate_secret_version(os.getenv("SECRET_NAME", "rotated-secret"), os.getenv("VERSION_ID"), os.getenv("STAGE")))
