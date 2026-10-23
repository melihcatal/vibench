import os
import json
from google.cloud import secretmanager

def parse_json_secret(project_id: str, secret_id: str):
    """
    Retrieves and parses a JSON-formatted secret from Google Secret Manager.

    Args:
        project_id: The Google Cloud project ID.
        secret_id: The ID of the secret to retrieve.

    Returns:
        A dictionary containing the parsed JSON secret payload.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"

    response = client.access_secret_version(name=name)
    secret_payload = response.payload.data.decode("UTF-8")

    return json.loads(secret_payload)

if __name__ == "__main__":
    # Example usage:
    # Set your Google Cloud project ID and secret ID
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    SECRET_ID = os.environ.get("GOOGLE_CLOUD_SECRET_ID")

    if not PROJECT_ID or not SECRET_ID:
        print("Please set GOOGLE_CLOUD_PROJECT_ID and GOOGLE_CLOUD_SECRET_ID environment variables.")
    else:
        try:
            parsed_secret = parse_json_secret(PROJECT_ID, SECRET_ID)
            print("Successfully parsed JSON secret:")
            print(json.dumps(parsed_secret, indent=2))
        except Exception as e:
            print(f"Error retrieving or parsing secret: {e}")
