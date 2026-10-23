from __future__ import annotations

import json
import os

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

from security_client import require_setting


def parse_json_secret(secret_name: str = "json-secret") -> dict:
    vault_url = require_setting("AZURE_KEY_VAULT_URL")
    client = SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())
    raw = client.get_secret(secret_name).value or "{}"
    return json.loads(raw)


if __name__ == "__main__":
    print(parse_json_secret(os.getenv("SECRET_NAME", "json-secret")))
