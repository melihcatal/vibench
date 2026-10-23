from security_client import SecretManagerClient
from security_models import parse_json_secret


def fetch_db_secret(secret_id: str = "DB_CREDENTIALS") -> dict:
    client = SecretManagerClient()
    secret_payload = client.get_secret_latest_version(secret_id)
    db_credentials = parse_json_secret(secret_payload)
    return db_credentials
