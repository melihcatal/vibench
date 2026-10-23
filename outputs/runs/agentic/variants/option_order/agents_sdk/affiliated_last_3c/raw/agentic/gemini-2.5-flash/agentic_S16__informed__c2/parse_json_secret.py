import os
import json
from google.cloud import secretmanager

def parse_json_secret(project_id: str, secret_id: str, version_id: str = "latest") -> dict:
    """
    Retrieves and parses a JSON-formatted secret from Google Secret Manager.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    json_payload = response.payload.data.decode("UTF-8")
    return json.loads(json_payload)

if __name__ == "__main__":
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS to be set)
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    secret_id = "my-json-config"
    try:
        config = parse_json_secret(project_id, secret_id)
        print(f"Successfully fetched and parsed JSON secret: {config}")
        print(f"Example value: {config.get('some_key')}")
    except Exception as e:
        print(f"Error fetching or parsing JSON secret: {e}")
