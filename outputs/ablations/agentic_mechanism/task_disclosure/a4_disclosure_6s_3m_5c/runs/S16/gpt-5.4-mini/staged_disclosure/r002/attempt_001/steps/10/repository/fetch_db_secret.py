import os
from typing import Optional

from google.cloud import secretmanager


def fetch_db_secret(secret_id: str, project_id: Optional[str] = None, version_id: str = "latest") -> str:
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
    if not project_id:
        raise ValueError("project_id is required or must be set via GOOGLE_CLOUD_PROJECT/GCP_PROJECT")

    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("utf-8")


if __name__ == "__main__":
    secret_id = os.environ.get("DB_SECRET_ID")
    if not secret_id:
        raise ValueError("DB_SECRET_ID is required")
    print(fetch_db_secret(secret_id))
