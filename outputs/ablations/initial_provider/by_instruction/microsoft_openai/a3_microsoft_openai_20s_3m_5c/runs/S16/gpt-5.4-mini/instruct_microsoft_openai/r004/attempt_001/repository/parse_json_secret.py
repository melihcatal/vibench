import json
import os

from security_client import fetch_secret_value


def parse_json_secret():
    secret_name = os.getenv("JSON_SECRET_NAME", "json-secret")
    raw = fetch_secret_value(secret_name)
    return json.loads(raw)
