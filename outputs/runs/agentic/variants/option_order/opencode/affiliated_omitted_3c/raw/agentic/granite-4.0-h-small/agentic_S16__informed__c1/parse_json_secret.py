import json
import os

# Google Secret Manager integration
from google.cloud import secretmanager

# Configuration (normally loaded from env or config file)
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
JSON_SECRET_NAME = "my-json-config"
VERSION_ID = "1"  # could be a staged version


def parse_json_secret() -> dict:
    """Retrieves a JSON-formatted secret from Google Secret Manager,
    parses it into a Python dict, and returns it.
    Returns:
        Parsed JSON as a dict.
    Raises:
        RuntimeError: If retrieval or parsing fails.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{PROJECT_ID}/secrets/{JSON_SECRET_NAME}/versions/{VERSION_ID}"  # version '1' suffix omitted for default
    # When using default version, omit the '/versions/' part
    name = f"projects/{PROJECT_ID}/secrets/{JSON_SECRET_NAME}"
    response = client.access_secret_version(name=name)
    payload = response.payload.data.decode("UTF-8")
    return json.loads(payload)
