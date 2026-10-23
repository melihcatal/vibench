from google.cloud import secretmanager
import json
import os

def parse_json_secret(project_id: str, secret_id: str, version_id: str = "latest"):
    """
    Retrieves and parses a JSON-formatted secret from Google Cloud Secret Manager.
    """
    client = secretmanager.SecretManagerServiceClient()

    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    response = client.access_secret_version(name=name)
    secret_payload = response.payload.data.decode("UTF-8")

    return json.loads(secret_payload)

if __name__ == "__main__":
    # Example usage:
    # Set these environment variables or replace with your actual values
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    secret_id = os.environ.get("GOOGLE_CLOUD_SECRET_ID")

    if not project_id or not secret_id:
        print("Please set GOOGLE_CLOUD_PROJECT_ID and GOOGLE_CLOUD_SECRET_ID environment variables.")
    else:
        try:
            parsed_secret = parse_json_secret(project_id, secret_id)
            print("Successfully retrieved and parsed JSON secret:")
            print(json.dumps(parsed_secret, indent=2))
        except Exception as e:
            print(f"Error accessing or parsing secret: {e}")
