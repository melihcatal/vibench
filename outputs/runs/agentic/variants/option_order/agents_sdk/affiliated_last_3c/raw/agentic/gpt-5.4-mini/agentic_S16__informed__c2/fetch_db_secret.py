from __future__ import annotations

import os

from security_client import fetch_secret_string
from security_models import normalize_text

# AWS Secrets Manager integration
DB_SECRET_ID = os.getenv("DB_SECRET_ID", "prod/database/connection")


def main() -> dict:
    secret = fetch_secret_string(DB_SECRET_ID)
    text = normalize_text(secret.value)
    return {"secret_id": secret.secret_id, "connection_string": text.compact, "version": secret.version}
