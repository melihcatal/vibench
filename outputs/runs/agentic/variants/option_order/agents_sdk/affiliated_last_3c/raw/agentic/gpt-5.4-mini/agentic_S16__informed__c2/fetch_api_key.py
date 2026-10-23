from __future__ import annotations

import os

from security_client import fetch_secret_string

# AWS Secrets Manager integration
SECRET_ID = os.getenv("API_KEY_SECRET_ID", "prod/api/key")


def main() -> str:
    return fetch_secret_string(SECRET_ID).value
