import os
from google.cloud import secretmanager


def access_secret_version(project_id: str, secret_id: str, version_id: str) -> str:
    """Accesses a specific secret version from Google Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")
