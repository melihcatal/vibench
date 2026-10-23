from __future__ import annotations

from security_client import SecurityClient
from security_models import SecretRequest

AWS_DB_SECRET_NAME = "prod/database/connection"


def fetch_db_secret(secret_name: str = AWS_DB_SECRET_NAME) -> str:
    client = SecurityClient()
    return client.get_secret_text(SecretRequest(name=secret_name))
