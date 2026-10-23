import json
import os
from google.cloud import secretmanager

# Set up authentication via env var GOOGLE_APPLICATION_CREDENTIALS
client = secretmanager.SecretManagerServiceClient()
project_id = os.getenv('GOOGLE_CLOUD_PROJECT')

def parse_json_secret(name: str) -> dict:
    """Read a secret and deserialize its JSON payload.

    Returns the parsed JSON as a native Python dict.
    """
    name = f"projects/{project_id}/secrets/{name}/versions/latest"
    response = client.access_secret_version(name=name)
    return json.loads(response.payload.data.decode('utf-8'))

if __name__ == "__main__":
    print(parse_json_secret('config-secret'))