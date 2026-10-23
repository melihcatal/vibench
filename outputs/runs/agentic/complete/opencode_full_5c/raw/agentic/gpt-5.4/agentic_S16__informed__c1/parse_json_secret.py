from __future__ import annotations

from typing import Any, Dict

from security_client import get_secret_client
from security_models import parse_json_secret_value


def parse_json_secret(secret_name: str, version: str | None = None) -> Dict[str, Any]:
    secret = get_secret_client().get_secret(secret_name, version=version)
    return parse_json_secret_value(secret.value)
