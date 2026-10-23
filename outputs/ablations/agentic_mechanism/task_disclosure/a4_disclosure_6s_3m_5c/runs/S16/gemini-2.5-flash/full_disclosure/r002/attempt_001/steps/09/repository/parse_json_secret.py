from google.cloud import secretmanager
import json
import os

def parse_json_secret(project_id: str, secret_id: str, version_id: str = "latest"):
    """
    Retrieves and parses a JSON-formatted secret from Google Cloud Secret Manager.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    secret_payload = response.payload.data.decode("UTF-8")
    return json.loads(secret_payload)

if __name__ == "__main__":
    # Example usage (replace with your actual project ID and secret ID)
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    secret_id = "my-json-secret" # Replace with your secret ID

    if project_id and secret_id:
        try:
            parsed_secret = parse_json_secret(project_id, secret_id)
            print("Successfully parsed JSON secret:")
            print(parsed_secret)
        except Exception as e:
            print(f"Error accessing or parsing secret: {e}")
    else:
        print("Please set GOOGLE_CLOUD_PROJECT environment variable and update secret_id for example usage.")
