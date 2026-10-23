import json

from security_client import load_secret_request, fetch_secret_value


def fetch_db_secret(secret_id: str):
    return json.loads(fetch_secret_value(load_secret_request(secret_id)).payload)
