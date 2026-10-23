import os
import json
from security_client import get_secret_manager_client
from security_models import SecretPayload


def parse_json_secret(
    project_id: str, secret_id: str, version_id: str = "latest"
) -> dict:
    """
    Retrieves and parses a JSON-formatted secret from Google Cloud Secret Manager.
    """
    client = get_secret_manager_client()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})

    payload = SecretPayload(raw=response.payload.data)
    return payload.as_json()


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    secret_id = "json-config-secret"
    json_secret = parse_json_secret(project_id, secret_id)
    print(f"Parsed JSON secret: {json_secret}")
