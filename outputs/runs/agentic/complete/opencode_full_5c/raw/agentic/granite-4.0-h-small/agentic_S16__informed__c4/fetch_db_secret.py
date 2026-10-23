import os
from google.cloud import secretmanager


def fetch_db_secret(project_id: str, secret_id: str) -> dict:
    """Fetch a database connection secret from Google Cloud Secret Manager.

    Args:
        project_id (str): Google Cloud project identifier.
        secret_id (str): Secret ID containing DB credentials.

    Returns:
        dict: Parsed secret JSON with connection details.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(name=name)
    # Assume secret value is a JSON string with db details
    import json

    return json.loads(response.payload.data.decode("UTF-8"))
