from __future__ import annotations

from security_client import decode_secret_value, get_secrets_manager_client, require_secret_id
from security_models import normalize_secret_response


def fetch_db_secret() -> dict:
    secret_id = require_secret_id("DB_SECRET_ID")
    client = get_secrets_manager_client()
    response = client.get_secret_value(SecretId=secret_id)
    payload = normalize_secret_response(secret_id, response, decode_secret_value(response))
    return payload.as_dict()
