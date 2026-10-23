from __future__ import annotations

import os
from typing import Any, Dict

from security_client import get_secret_value
from security_models import normalize_secret_value, parse_json_secret as parse_json_payload

AWS_SECRET_ID = os.getenv("JSON_SECRET_ID", "prod/json-config")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")


def retrieve_and_parse_json_secret() -> Dict[str, Any]:
    payload = get_secret_value(AWS_SECRET_ID, region_name=AWS_REGION)
    secret = normalize_secret_value(AWS_SECRET_ID, payload)
    return parse_json_payload(secret.as_text())
