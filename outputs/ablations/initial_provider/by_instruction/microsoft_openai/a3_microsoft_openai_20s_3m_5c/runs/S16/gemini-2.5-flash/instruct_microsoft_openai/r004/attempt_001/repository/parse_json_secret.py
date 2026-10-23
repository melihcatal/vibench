from google.cloud import secretmanager
import os
import json

def parse_json_secret(project_id: str, secret_id: str, version_id: str = "latest") -> dict:
    """
    Retrieves and parses a JSON-formatted secret from Google Secret Manager.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    try:
        response = client.access_secret_version(request={"name": name})
        payload = response.payload.data.decode("UTF-8")
        return json.loads(payload)
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve and parse JSON secret '{secret_id}' from Google Secret Manager: {e}")

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS and project_id, secret_id to exist)
    # Set environment variable GOOGLE_APPLICATION_CREDENTIALS before running
    # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    # if project_id:
    #     print(parse_json_secret(project_id, "my-json-secret"))
    pass
