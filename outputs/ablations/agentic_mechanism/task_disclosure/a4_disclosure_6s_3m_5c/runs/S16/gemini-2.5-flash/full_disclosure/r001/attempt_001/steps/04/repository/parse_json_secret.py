import json
from google.cloud import secretmanager

def get_json_secret(project_id: str, secret_id: str, version_id: str = "latest") -> dict:
    """
    Retrieves and parses a JSON-formatted secret from Google Cloud Secret Manager.

    Args:
        project_id: The Google Cloud project ID.
        secret_id: The ID of the secret to retrieve.
        version_id: The version of the secret to retrieve (e.g., "latest", "1", "2").

    Returns:
        A dictionary containing the parsed JSON secret.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("UTF-8")
    return json.loads(payload)
