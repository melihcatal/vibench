import json
import os

from security_client import (
    build_secrets_manager_client,
    fetch_secret_payload,
    secret_request,
)
from security_models import parse_json_secret as normalize_json_secret


def parse_json_secret(secret_name: str = None, version: str = None) -> dict:
    request = secret_request(
        secret_name or os.environ["JSON_SECRET_NAME"], version=version
    )
    response = fetch_secret_payload(request, build_secrets_manager_client())
    return normalize_json_secret(response.value)
