from security_client import access_secret_version
import json
import os


def parse_json_secret(project_id: str, secret_id: str) -> dict:
    """Retrieves and parses a JSON-formatted secret from Google Secret Manager."""
    # GOOGLE_APPLICATION_CREDENTIALS environment variable is used for authentication
    # The GOOGLE_CLOUD_PROJECT environment variable should be set for the project_id
    project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError(
            "Google Cloud project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable."
        )
    secret_payload = access_secret_version(project_id, secret_id)
    return json.loads(secret_payload)
