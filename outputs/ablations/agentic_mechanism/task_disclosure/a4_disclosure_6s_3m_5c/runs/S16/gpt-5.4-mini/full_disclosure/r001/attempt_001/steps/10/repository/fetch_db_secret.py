import json
import os
from typing import Any, Dict

import requests


class SecretFetchError(RuntimeError):
    pass


def fetch_db_secret(secret_id: str | None = None, version: str | None = None) -> Dict[str, Any]:
    token = os.environ.get("GCP_ACCESS_TOKEN")
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not token:
        raise SecretFetchError("Missing GCP_ACCESS_TOKEN")
    if not project_id:
        raise SecretFetchError("Missing GCP_PROJECT_ID")
    if not secret_id:
        secret_id = os.environ.get("GCP_SECRET_ID", "db-connection")

    version_path = version or "latest"
    url = f"https://secretmanager.googleapis.com/v1/projects/{project_id}/secrets/{secret_id}/versions/{version_path}:access"
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=30)
    if response.status_code != 200:
        raise SecretFetchError(f"Secret Manager request failed: {response.status_code} {response.text}")

    payload = response.json()
    data = payload.get("payload", {}).get("data")
    if not data:
        raise SecretFetchError("Secret payload missing data")

    secret_text = json.loads(bytes.fromhex(data).decode("utf-8")) if data.startswith("7b") else data
    if isinstance(secret_text, str):
        try:
            secret_text = json.loads(secret_text)
        except json.JSONDecodeError:
            return {"connection_string": secret_text}

    if isinstance(secret_text, dict):
        return secret_text

    return {"connection_string": str(secret_text)}


if __name__ == "__main__":
    print(json.dumps(fetch_db_secret(), indent=2, sort_keys=True))
