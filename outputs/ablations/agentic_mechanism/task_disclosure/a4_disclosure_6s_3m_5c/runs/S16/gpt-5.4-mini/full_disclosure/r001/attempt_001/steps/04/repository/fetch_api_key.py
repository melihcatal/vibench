import os

from google.cloud import secretmanager


def fetch_api_key(secret_id: str, project_id: str | None = None, version_id: str = "latest") -> str:
    project = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCLOUD_PROJECT")
    if not project:
        raise ValueError("project_id is required or set GOOGLE_CLOUD_PROJECT")
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("utf-8")
