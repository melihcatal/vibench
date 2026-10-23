import os
from google.cloud import secretmanager

def fetch_db_secret(project_id: str, secret_id: str) -> dict:
    """Fetches a database connection secret from Google Secret Manager.

    The secret payload is expected to be a JSON string containing at least
    'username', 'password', and 'host'. This example returns a Python dict.

    Args:
        project_id (str): GCP project ID.
        secret_id (str): Secret name.

    Returns:
        dict: Database credentials.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(name=name)
    payload = response.payload.data.decode('UTF-8')
    return json.loads(payload)
