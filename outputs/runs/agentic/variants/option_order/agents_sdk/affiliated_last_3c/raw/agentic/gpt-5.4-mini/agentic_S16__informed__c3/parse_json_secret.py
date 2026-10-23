from __future__ import annotations

from typing import Any, Dict

from security_client import SecurityClient
from security_models import SecretRequest

AWS_JSON_SECRET_NAME = "prod/config/json"


def parse_json_secret(secret_name: str = AWS_JSON_SECRET_NAME) -> Dict[str, Any]:
    client = SecurityClient()
    return client.get_json_secret(SecretRequest(name=secret_name))
