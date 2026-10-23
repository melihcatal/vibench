from security_client import GoogleSecretManagerClient
import os
import json


def parse_json_secret(secret_id: str) -> dict:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")

    client = GoogleSecretManagerClient(project_id)
    secret_value = client.get_secret(secret_id)
    return json.loads(secret_value)
