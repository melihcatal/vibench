import os
import json
from google.cloud import secretmanager

def parse_json_secret(project_id: str, secret_id: str, version_id: str = "latest") -> dict:
    """
    Retrieves and parses a JSON-formatted secret from Google Secret Manager.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(name=name)
    secret_payload = response.payload.data.decode("UTF-8")
    return json.loads(secret_payload)

if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    json_secret_id = "my-json-config" # Replace with your secret ID containing JSON

    if project_id:
        try:
            json_data = parse_json_secret(project_id, json_secret_id)
            print(f"Successfully parsed JSON secret: {json_data}")
            print(f"Example value from JSON: {json_data.get('username')}")
        except Exception as e:
            print(f"Error parsing JSON secret: {e}")
    else:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
