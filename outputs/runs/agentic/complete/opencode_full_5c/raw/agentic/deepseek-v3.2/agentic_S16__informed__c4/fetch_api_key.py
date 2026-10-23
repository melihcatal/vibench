import os
from google.cloud import secretmanager


def fetch_api_key(secret_name: str, project_id: str = None) -> str:
    """Fetch an API key from Google Cloud Secret Manager."""
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError(
                "Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable"
            )

    client = secretmanager.SecretManagerServiceClient()
    secret_version_name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"

    response = client.access_secret_version(request={"name": secret_version_name})
    api_key = response.payload.data.decode("UTF-8")

    return api_key
