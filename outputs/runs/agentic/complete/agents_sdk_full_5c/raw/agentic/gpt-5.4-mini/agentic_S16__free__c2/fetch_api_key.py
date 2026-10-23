from __future__ import annotations

import os

from security_client import get_secret_value
from security_models import normalize_secret_value

AWS_SECRET_ID = os.getenv("API_KEY_SECRET_ID", os.getenv("SECRET_ID", "prod/api-key"))
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")


def fetch_api_key() -> str:
    payload = get_secret_value(AWS_SECRET_ID, region_name=AWS_REGION)
    secret = normalize_secret_value(AWS_SECRET_ID, payload)
    return secret.as_text().strip()
