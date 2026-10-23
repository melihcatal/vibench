import os
from google.cloud import secretmanager

def fetch_db_secret(project_id: str, secret_id: str, version: str = "latest") -> dict:
    """Fetches a database connection secret (username, password, host, etc.) from Google Secret Manager.

    Args:
        project_id: GCP project identifier.
        secret_id: Identifier of the secret containing DB credentials JSON.
        version: Specific version to retrieve (default 'latest').

    Returns:
        A dict with parsed JSON fields (e.g., {'username': ..., 'password': ..., 'host': ...}).
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version}"
    response = client.access_secret_version(name=name)
    payload = response.payload.data.decode('UTF-8')
    return json.loads(payload)
