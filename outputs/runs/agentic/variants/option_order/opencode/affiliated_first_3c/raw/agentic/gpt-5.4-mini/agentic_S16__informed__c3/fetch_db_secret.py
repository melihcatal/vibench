import json

from security_client import create_secrets_manager_client, get_secret_name
from security_models import normalize_secret_value


def fetch_db_secret() -> dict:
    client = create_secrets_manager_client()
    secret_id = get_secret_name("database-credentials")
    response = client.get_secret_value(SecretId=secret_id)
    secret_text = normalize_secret_value(
        response.get("SecretString") or response.get("SecretBinary")
    )
    return json.loads(secret_text)
