import os
import json
from typing import Optional

from google.cloud import secretmanager


def fetch_api_key() -> str:
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    secret_id = os.environ["GOOGLE_SECRET_MANAGER_API_KEY_SECRET_ID"]
    version = os.getenv("GOOGLE_SECRET_MANAGER_API_KEY_VERSION", "latest")
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version}"
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("utf-8").strip()
    try:
        parsed = json.loads(payload)
        if isinstance(parsed, dict) and "api_key" in parsed:
            value = parsed["api_key"]
            if not isinstance(value, str):
                raise ValueError("api_key must be a string")
            return value
    except json.JSONDecodeError:
        pass
    return payload


if __name__ == "__main__":
    print(fetch_api_key())
