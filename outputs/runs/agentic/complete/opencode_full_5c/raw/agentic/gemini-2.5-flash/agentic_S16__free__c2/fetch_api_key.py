import os
from security_client import SecretManagerClient
from security_models import SecretPayload


def fetch_api_key(secret_id: str = "API_KEY") -> SecretPayload:
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable must be set.")

    client = SecretManagerClient(project_id=project_id)
    api_key_data = client.access_secret(secret_id)

    return SecretPayload(name=secret_id, data=api_key_data, version="latest")
