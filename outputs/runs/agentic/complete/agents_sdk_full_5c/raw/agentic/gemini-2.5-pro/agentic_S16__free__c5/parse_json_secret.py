
import os
import json
from google.cloud import secretmanager
from security_models import DatabaseCredentials

def get_and_parse_json_secret(project_id: str, secret_id: str, version_id: str = "latest") -> DatabaseCredentials | None:
    """
    Retrieves a secret from Google Cloud Secret Manager, parses it as JSON,
    and returns a structured object.

    Args:
        project_id: The Google Cloud project ID.
        secret_id: The ID of the secret.
        version_id: The version of the secret to access.

    Returns:
        A DatabaseCredentials object, or None if an error occurs.
    """
    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

        response = client.access_secret_version(request={"name": name})
        payload = response.payload.data.decode("UTF-8")
        
        secret_data = json.loads(payload)
        
        return DatabaseCredentials(**secret_data)

    except Exception as e:
        print(f"Error accessing or parsing secret: {e}")
        return None

if __name__ == '__main__':
    # Example usage:
    # Ensure you are authenticated with Google Cloud CLI: `gcloud auth application-default login`
    GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
    JSON_SECRET_ID = os.environ.get("GCP_JSON_SECRET_ID", "db-credentials-json")

    if not GCP_PROJECT_ID:
        print("GCP_PROJECT_ID environment variable not set.")
    else:
        credentials = get_and_parse_json_secret(GCP_PROJECT_ID, JSON_SECRET_ID)
        if credentials:
            print("Successfully fetched and parsed JSON secret.")
            print(f"Username: {credentials.username}")
        else:
            print("Failed to fetch or parse JSON secret.")
