import os
import json
from security_client import SecretManagerClient
from security_models import SecretRequest


def parse_json_secret(project_id: str, secret_id: str) -> dict:
    client = SecretManagerClient()
    request = SecretRequest(project_id=project_id, secret_id=secret_id)
    response = client.access_secret_version(request)
    return json.loads(response.payload)


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    json_secret_id = "my-json-config"
    if project_id:
        json_config = parse_json_secret(project_id, json_secret_id)
        print(f"Parsed JSON Secret: {json_config}")
    else:
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable.")
