import json
import os

from security_client import (
    build_secrets_manager_client,
    fetch_secret_payload,
    secret_request,
)


def fetch_db_secret(secret_name: str = None, stage: str = None) -> dict:
    request = secret_request(secret_name or os.environ["DB_SECRET_NAME"], stage=stage)
    response = fetch_secret_payload(request, build_secrets_manager_client())
    return json.loads(response.value)
