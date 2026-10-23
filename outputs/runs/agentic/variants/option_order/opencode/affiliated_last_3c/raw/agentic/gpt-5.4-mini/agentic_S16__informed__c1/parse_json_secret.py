import json
import os

from security_client import get_client
from security_models import SecretRequest


def parse_json_secret(secret_name: str | None = None) -> dict:
    client = get_client()
    request = SecretRequest(secret_name=secret_name or os.environ["JSON_SECRET_NAME"])
    value = client.fetch(request).value
    if isinstance(value, str):
        return json.loads(value)
    return dict(value)
