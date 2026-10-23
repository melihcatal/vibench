import os

from security_client import build_secrets_client, get_secret_string
from security_models import SecretRequest, normalize_secret_payload


def fetch_db_secret():
    secret_id = os.environ["DB_SECRET_ID"]
    request = SecretRequest(secret_id=secret_id)
    client = build_secrets_client()
    secret_string = get_secret_string(client, request.secret_id)
    return normalize_secret_payload(secret_string)
