from __future__ import annotations

import json
from typing import Any, Dict

from security_client import get_secret_value
from security_models import SecretRequest


def fetch_db_secret(secret_name: str, region: str | None = None) -> Dict[str, Any]:
    response = get_secret_value(SecretRequest(secret_name=secret_name, region=region))
    payload = response.value
    return json.loads(payload) if payload.strip().startswith("{") else {"connection_string": payload}
