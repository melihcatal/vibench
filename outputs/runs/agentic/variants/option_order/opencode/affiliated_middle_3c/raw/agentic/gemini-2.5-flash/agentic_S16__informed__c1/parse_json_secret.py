import os
import json
from google.cloud import secretmanager


def parse_json_secret(
    project_id: str, secret_id: str, version_id: str = "latest"
) -> dict:
    """
    Retrieves and parses a JSON-formatted secret from Google Secret Manager.
    Provider: Google Cloud Secret Manager
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    secret_payload = response.payload.data.decode("UTF-8")
    return json.loads(secret_payload)


if __name__ == "__main__":
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS to be set)
    # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    # secret_id = "my-json-secret"
    # json_secret = parse_json_secret(project_id, secret_id)
    # print(f"Parsed JSON Secret: {json_secret}")
    pass
