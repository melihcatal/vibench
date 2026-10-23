import os
import json
from google.cloud import secretmanager


def fetch_db_secret(secret_id: str | None = None, project_id: str | None = None, version: str = "latest") -> str:
    if secret_id is None:
        secret_id = os.environ.get("DB_SECRET_ID")
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
    if not secret_id or not project_id:
        raise ValueError("DB_SECRET_ID and GOOGLE_CLOUD_PROJECT (or GCP_PROJECT) are required")

    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version}"
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("utf-8")

    try:
        parsed = json.loads(payload)
        if isinstance(parsed, dict) and "connection_string" in parsed:
            return parsed["connection_string"]
    except json.JSONDecodeError:
        pass

    return payload
