import os
import json

# Provider-specific configuration
# Using Google Cloud Secret Manager
GCLOUD_PROJECT = os.getenv("GCLOUD_PROJECT")
GCLOUD_APPLICATION_CREDENTIALS = os.getenv("GCLOUD_APPLICATION_CREDENTIALS")

from google.cloud import secretmanager

client = secretmanager.SecretManagerServiceClient()


def retrieve_secret(secret_name: str) -> str:
    """Retrieve a secret payload from Google Secret Manager.
    Returns the raw payload string.
    """
    name = f"projects/{GCLOUD_PROJECT}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(name=name)
    payload = response.payload.data.decode("UTF-8")
    return payload  # Assume JSON string


def parse_json_secret(secret_name: str) -> dict:
    """Retrieve and parse a JSON-formatted secret from Google Secret Manager.
    Returns a dict with the parsed JSON.
    """
    raw = retrieve_secret(secret_name)
    return json.loads(raw)


if __name__ == "__main__":
    secret_name = os.getenv("JSON_SECRET_NAME")
    if secret_name:
        print("Parsed JSON secret:", parse_json_secret(secret_name))
    else:
        print("Set JSON_SECRET_NAME env var")
