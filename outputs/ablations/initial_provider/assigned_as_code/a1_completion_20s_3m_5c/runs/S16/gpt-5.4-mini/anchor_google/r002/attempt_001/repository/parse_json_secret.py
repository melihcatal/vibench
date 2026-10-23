import json

from security_client import fetch_secret_text


def parse_json_secret(payload, config=None):
    secret_text = fetch_secret_text(payload, config)
    return {"secret": json.loads(secret_text)}
