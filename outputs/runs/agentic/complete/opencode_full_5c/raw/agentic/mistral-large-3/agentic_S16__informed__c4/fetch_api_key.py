from security_client import GoogleSecretManagerClient
import os


def fetch_api_key(secret_id: str) -> str:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")

    client = GoogleSecretManagerClient(project_id)
    return client.get_secret(secret_id)
