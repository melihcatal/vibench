from __future__ import annotations

from typing import Any, Dict

from security_client import get_secret_value, parse_json_payload
from security_models import SecretRequest


def parse_json_secret(secret_name: str, region: str | None = None) -> Dict[str, Any]:
    response = get_secret_value(SecretRequest(secret_name=secret_name, region=region))
    return parse_json_payload(response.value)
