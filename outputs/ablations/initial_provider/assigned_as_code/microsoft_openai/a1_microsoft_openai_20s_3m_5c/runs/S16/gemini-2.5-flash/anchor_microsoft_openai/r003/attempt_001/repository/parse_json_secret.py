import json
from google.cloud import secretmanager

def parse_json_secret(project_id: str, secret_id: str, version_id: str = "latest") -> dict:
    """
    Retrieves and parses a JSON-formatted secret from Google Cloud Secret Manager.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    secret_data = response.payload.data.decode("UTF-8")
    return json.loads(secret_data)
