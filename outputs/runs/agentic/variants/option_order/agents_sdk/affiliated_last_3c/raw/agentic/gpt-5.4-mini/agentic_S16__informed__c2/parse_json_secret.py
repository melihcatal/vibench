from __future__ import annotations

import os

from security_client import fetch_secret_json

# AWS Secrets Manager integration
JSON_SECRET_ID = os.getenv("JSON_SECRET_ID", "prod/config/json")


def main() -> dict:
    return fetch_secret_json(JSON_SECRET_ID)
