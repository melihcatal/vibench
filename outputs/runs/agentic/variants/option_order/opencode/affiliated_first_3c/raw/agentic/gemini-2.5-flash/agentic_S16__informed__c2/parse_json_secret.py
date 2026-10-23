import json
from google.cloud import secretmanager
import os


def parse_json_secret(project_id: str, secret_id: str) -> dict:
    """Retrieves and parses a JSON-formatted secret from Google Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(name=name)
    secret_payload = response.payload.data.decode("UTF-8")
    return json.loads(secret_payload)


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    json_secret_id = os.environ.get("JSON_SECRET_ID", "my-json-secret")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    json_secret = parse_json_secret(project_id, json_secret_id)
    print(f"Parsed JSON Secret: {json_secret}")
