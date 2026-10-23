from __future__ import annotations

from security_client import decode_secret_value, get_secrets_manager_client, require_secret_id
from security_models import parse_secret_json


def parse_json_secret() -> dict:
    secret_id = require_secret_id("JSON_SECRET_ID")
    client = get_secrets_manager_client()
    response = client.get_secret_value(SecretId=secret_id)
    secret_json = parse_secret_json(decode_secret_value(response))
    return {
        "secret_id": secret_id,
        "version_id": response.get("VersionId"),
        "data": secret_json,
    }
