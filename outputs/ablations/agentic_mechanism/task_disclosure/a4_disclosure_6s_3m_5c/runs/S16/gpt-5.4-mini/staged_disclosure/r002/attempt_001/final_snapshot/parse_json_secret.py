import json
import os
from typing import Any, Dict, Optional

import requests


VAULT_API_BASE_URL = os.environ.get("VAULT_API_BASE_URL", "https://api.vaultproject.io")
VAULT_TOKEN = os.environ.get("VAULT_TOKEN")
VAULT_SECRET_PATH = os.environ.get("VAULT_SECRET_PATH")


def retrieve_secret() -> str:
    if not VAULT_TOKEN:
        raise RuntimeError("VAULT_TOKEN is required")
    if not VAULT_SECRET_PATH:
        raise RuntimeError("VAULT_SECRET_PATH is required")

    url = f"{VAULT_API_BASE_URL.rstrip('/')}/v1/{VAULT_SECRET_PATH.lstrip('/')}"
    response = requests.get(
        url,
        headers={"X-Vault-Token": VAULT_TOKEN},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()

    if isinstance(payload, dict):
        data = payload.get("data")
        if isinstance(data, dict):
            if "value" in data and isinstance(data["value"], str):
                return data["value"]
            if "secret" in data and isinstance(data["secret"], str):
                return data["secret"]
            if "json" in data and isinstance(data["json"], str):
                return data["json"]
            if "data" in data and isinstance(data["data"], str):
                return data["data"]

    if isinstance(payload, str):
        return payload

    raise ValueError("Secret response did not contain a retrievable secret string")


def parse_json_secret(secret_text: Optional[str] = None) -> Dict[str, Any]:
    raw = retrieve_secret() if secret_text is None else secret_text
    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise ValueError("Secret JSON must decode to an object")
    return parsed


if __name__ == "__main__":
    print(json.dumps(parse_json_secret(), sort_keys=True))
