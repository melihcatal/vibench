import os
from typing import Optional

import requests


class SecretRotationError(RuntimeError):
    pass


class GoogleSecretManagerClient:
    def __init__(self, project_id: str, access_token: str) -> None:
        self.project_id = project_id
        self.access_token = access_token
        self.base_url = "https://secretmanager.googleapis.com/v1"

    def access_secret_version(self, secret_id: str, version: str) -> str:
        url = f"{self.base_url}/projects/{self.project_id}/secrets/{secret_id}/versions/{version}:access"
        response = requests.get(
            url,
            headers={"Authorization": f"Bearer {self.access_token}"},
            timeout=30,
        )
        if response.status_code != 200:
            raise SecretRotationError(f"Google Secret Manager request failed: {response.status_code} {response.text}")
        payload = response.json()
        data = payload.get("payload", {}).get("data")
        if not data:
            raise SecretRotationError("Secret payload missing data")
        return bytes.fromhex(data).decode("utf-8") if data.startswith("7b") else data


def rotate_secret_version(secret_id: Optional[str] = None, version: Optional[str] = None, stage: Optional[str] = None) -> str:
    project_id = os.environ.get("GCP_PROJECT_ID") or os.environ.get("GOOGLE_CLOUD_PROJECT")
    access_token = os.environ.get("GCP_ACCESS_TOKEN")
    if not project_id:
        raise SecretRotationError("Missing GCP_PROJECT_ID or GOOGLE_CLOUD_PROJECT")
    if not access_token:
        raise SecretRotationError("Missing GCP_ACCESS_TOKEN")

    secret_name = secret_id or os.environ.get("GCP_SECRET_ID")
    if not secret_name:
        raise SecretRotationError("Missing secret_id or GCP_SECRET_ID")

    version_ref = version or stage or os.environ.get("GCP_SECRET_VERSION") or os.environ.get("GCP_SECRET_STAGE") or "latest"
    client = GoogleSecretManagerClient(project_id=project_id, access_token=access_token)
    return client.access_secret_version(secret_id=secret_name, version=version_ref)
