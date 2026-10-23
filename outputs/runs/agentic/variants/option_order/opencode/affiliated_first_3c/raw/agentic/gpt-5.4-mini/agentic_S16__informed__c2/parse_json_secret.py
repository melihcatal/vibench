import json
import os

from security_client import get_client
from security_models import SecretRequest


def parse_json_secret(secret_name: str | None = None):
    client = get_client()
    request = SecretRequest(
        name=secret_name or os.getenv("JSON_SECRET_NAME", "json/secret")
    )
    payload = client.get_secret(request).value
    return json.loads(payload if isinstance(payload, str) else payload.decode())
