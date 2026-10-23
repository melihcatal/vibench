import os
import json

from security_client import get_client
from security_models import SecretRequest


def fetch_db_secret(secret_name: str | None = None):
    client = get_client()
    request = SecretRequest(
        name=secret_name or os.getenv("DB_SECRET_NAME", "database/connection")
    )
    secret = client.get_secret(request).value
    if isinstance(secret, str):
        return json.loads(secret)
    return secret
