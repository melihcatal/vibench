import google.cloud.secretmanager as secretmanager
import json

def parse_json_secret(project_id: str, secret_id: str):
    """
    Retrieves and parses a JSON-formatted secret from Google Cloud Secret Manager.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(name=name)
    secret_payload = response.payload.data.decode("UTF-8")
    return json.loads(secret_payload)
