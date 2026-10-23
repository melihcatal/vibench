from __future__ import annotations

import os
from typing import Dict

from security_client import get_secret_value
from security_models import normalize_secret_value, parse_json_secret

AWS_SECRET_ID = os.getenv("DB_SECRET_ID", "prod/database")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")


def fetch_db_secret() -> Dict[str, str]:
    payload = get_secret_value(AWS_SECRET_ID, region_name=AWS_REGION)
    secret = normalize_secret_value(AWS_SECRET_ID, payload)
    data = parse_json_secret(secret.as_text())
    return {str(k): str(v) for k, v in data.items()}
