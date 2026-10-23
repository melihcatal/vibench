import os
from security_client import SecretManagerClient
from security_models import Secret


def fetch_db_secret(secret_id: str, project_id: str = None) -> Secret:
    client = SecretManagerClient(project_id=project_id)
    db_secret = client.access_secret_version(secret_id=secret_id)
    return db_secret
