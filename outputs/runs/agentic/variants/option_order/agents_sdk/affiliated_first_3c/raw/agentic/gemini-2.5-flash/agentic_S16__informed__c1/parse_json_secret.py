from google.cloud import secretmanager
import json
import os

def parse_json_secret(project_id: str, secret_id: str) -> dict:
    """
    Retrieves and parses a JSON-formatted secret from Google Secret Manager.
    Requires GOOGLE_APPLICATION_CREDENTIALS or gcloud auth.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"

    try:
        response = client.access_secret_version(request={"name": name})
        secret_payload = response.payload.data.decode("UTF-8")
        return json.loads(secret_payload)
    except Exception as e:
        print(f"Error accessing or parsing secret '{secret_id}': {e}")
        raise

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS or gcloud auth)
    # os.environ['GOOGLE_CLOUD_PROJECT'] = 'your-gcp-project-id'
    # os.environ['JSON_SECRET_ID'] = 'your-json-secret-name'
    project_id = os.environ.get('GOOGLE_CLOUD_PROJECT', 'your-gcp-project-id')
    secret_id = os.environ.get('JSON_SECRET_ID', 'your-json-secret-name')
    try:
        parsed_secret = parse_json_secret(project_id, secret_id)
        print(f"Successfully parsed JSON secret: {parsed_secret}")
    except Exception:
        print("Failed to parse JSON secret.")
