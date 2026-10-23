import json
import os

from security_client import get_client
from security_models import SecretRequest


def fetch_db_secret(secret_name: str | None = None) -> dict:
    client = get_client()
    request = SecretRequest(secret_name=secret_name or os.environ["DB_SECRET_NAME"])
    value = client.fetch(request).value
    return json.loads(value) if isinstance(value, str) else dict(value)
