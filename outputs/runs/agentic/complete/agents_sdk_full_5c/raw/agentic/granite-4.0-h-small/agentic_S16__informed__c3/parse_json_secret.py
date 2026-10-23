import json
from google.cloud import secretmanager

def parse_json_secret(project_id: str, secret_id: str) -> dict:
    """Retrieves a secret and parses its JSON payload.

    Args:
        project_id (str): GCP project ID.
        secret_id (str): Secret name.

    Returns:
        dict: Parsed JSON data stored in the secret.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(name=name)
    return json.loads(response.payload.data.decode('UTF-8'))
