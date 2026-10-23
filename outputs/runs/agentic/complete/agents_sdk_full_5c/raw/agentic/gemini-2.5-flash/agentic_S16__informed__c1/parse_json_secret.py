from google.cloud import secretmanager
import json
import os

def parse_json_secret(project_id: str, secret_id: str) -> dict:
    """Retrieves and parses a JSON-formatted secret from Google Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    secret_payload = response.payload.data.decode("UTF-8")
    return json.loads(secret_payload)

if __name__ == "__main__":
    # Example usage (replace with actual project_id and secret_id)
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    json_secret_id = os.environ.get("JSON_SECRET_ID", "my-json-config")
    try:
        json_data = parse_json_secret(project_id, json_secret_id)
        print(f"Parsed JSON Secret: {json_data}")
    except Exception as e:
        print(f"Error parsing JSON secret: {e}")
