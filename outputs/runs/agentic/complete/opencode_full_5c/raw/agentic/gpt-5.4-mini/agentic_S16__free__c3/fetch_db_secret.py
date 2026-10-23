import os

from security_client import get_secrets_client, normalize_secret_response


def fetch_db_secret(secret_id: str = None):
    client = get_secrets_client()
    secret_id = secret_id or os.getenv("AWS_SECRET_DB_ID", "database/connection")
    response = client.get_secret_value(SecretId=secret_id)
    secret = normalize_secret_response(response)
    return secret.get("SecretString")
