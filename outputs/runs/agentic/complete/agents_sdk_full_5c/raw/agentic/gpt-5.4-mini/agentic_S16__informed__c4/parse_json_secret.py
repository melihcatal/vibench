from __future__ import annotations

from typing import Any, Dict

from security_client import SecretManagerClientHelper
from security_models import parse_json_secret_payload


def parse_json_secret(secret_name: str, version: str = "latest") -> Dict[str, Any]:
    helper = SecretManagerClientHelper()
    payload = helper.access_secret(secret_name, version)
    return parse_json_secret_payload(payload)
