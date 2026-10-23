import os
from google.cloud import secretmanager

def fetch_db_secret(project_id: str, secret_id: str, version_id: str = "latest") -> str:
    """Fetches a database connection secret from Google Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    try:
        response = client.access_secret_version(request={"name": name})
        payload = response.payload.data.decode("UTF-8")
        return payload
    except Exception as e:
        raise ValueError(f"Error accessing secret '{secret_id}' in project '{project_id}': {e}") from e
