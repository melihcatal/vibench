import os
import json
from google.cloud import secretmanager
from security_client import parse_google_credentials

# Configure Google Cloud Secret Manager client
credentials = parse_google_credentials()
client = secretmanager.SecretManagerServiceClient(credentials=credentials)
project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")


def parse_json_secret(name: str):
    """Retrieve and parse a JSON-formatted secret from Google Secret Manager.

    Args:
        name (str): The fully qualified secret ID in the format
                    `projects/<PROJECT>/secrets/<NAME>/versions/latest`.

    Returns:
        dict: Parsed JSON content of the secret.
    """
    try:
        response = client.access_secret_version(name=name)
        payload = response.payload.data.decode("utf-8")
        return json.loads(payload)
    except Exception as exc:
        raise RuntimeError(f"Error reading secret {name}: {exc}")


if __name__ == "__main__":
    # Example usage: pass the secret ID as first argument
    import sys

    secret_id = sys.argv[1] if len(sys.argv) > 1 else os.getenv("GOOGLE_SECRET_ID")
    parsed = parse_json_secret(secret_id)
    print(json.dumps(parsed, indent=2))
