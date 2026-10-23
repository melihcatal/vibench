import os
import json
from google.cloud import secretmanager

def parse_json_secret(project_id: str, secret_id: str) -> dict:
    """
    Retrieves and parses a JSON-formatted secret from Google Cloud Secret Manager.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    secret_payload = response.payload.data.decode("UTF-8")
    return json.loads(secret_payload)

if __name__ == "__main__":
    # Example usage (replace with actual project_id and secret_id)
    project_id = os.getenv("GCP_PROJECT_ID")
    json_secret_id = "my-json-config"
    if project_id:
        try:
            json_config = parse_json_secret(project_id, json_secret_id)
            print(f"Fetched JSON Config: {json_config}")
            print(f"Accessing a key (e.g., 'user'): {json_config.get('user')}")
        except Exception as e:
            print(f"Error fetching or parsing JSON secret: {e}")
    else:
        print("GCP_PROJECT_ID environment variable not set.")
