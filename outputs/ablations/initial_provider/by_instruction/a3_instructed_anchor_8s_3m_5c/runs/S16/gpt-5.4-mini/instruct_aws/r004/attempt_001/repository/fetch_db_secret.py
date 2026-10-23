from security_client import load_secret_name, secrets_manager_client
from security_models import normalize_secret_payload


def fetch_db_secret(secret_name: str = None):
    client = secrets_manager_client()
    secret_id = secret_name or load_secret_name("database/credentials")
    response = client.get_secret_value(SecretId=secret_id)
    return normalize_secret_payload(response)["value"]
