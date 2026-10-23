from security_client import SecretManagerClient
from security_models import DatabaseSecret


def fetch_db_secret(secret_id: str) -> DatabaseSecret:
    """Fetches a database connection secret from Google Secret Manager."""
    client = SecretManagerClient()
    secret_payload = client.access_secret_version(secret_id)
    return DatabaseSecret.from_json_string(secret_id, secret_payload)
