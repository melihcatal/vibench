from security_client import SecretManagerClient
from security_models import SecretResponse, normalize_secret_response
import os


def fetch_db_secret(secret_id: str = "DB_CONNECTION_SECRET") -> SecretResponse:
    client = SecretManagerClient()
    secret_value = client.get_secret_latest(secret_id)
    version_id = client.list_secret_versions(secret_id)[0]
    return normalize_secret_response(
        secret_id=secret_id,
        version_id=version_id,
        secret_value=secret_value,
        labels={"provider": "google-cloud-secret-manager", "type": "db-secret"},
        notes="PostgreSQL connection string for analytics database",
    )
