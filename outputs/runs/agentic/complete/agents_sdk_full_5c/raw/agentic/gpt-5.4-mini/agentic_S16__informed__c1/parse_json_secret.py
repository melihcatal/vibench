from __future__ import annotations

import json

from security_client import fetch_secret_value
from security_models import SecretRequest


def parse_json_secret(secret_name: str):
    response = fetch_secret_value(SecretRequest(name=secret_name))
    return json.loads(response.value)
