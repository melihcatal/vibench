import os
from security_client import SecretManagerClient
from security_models import SecretPayload


def fetch_db_secret(secret_id: str = "DATABASE_CREDENTIALS") -> SecretPayload:
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable must be set.")

    client = SecretManagerClient(project_id=project_id)
    db_secret_data = client.access_secret(secret_id)

    return SecretPayload(name=secret_id, data=db_secret_data, version="latest")
