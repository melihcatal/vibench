import os
import json
from typing import Any, Optional
from security_client import build_secret_request, fetch_secret
from security_models import SecretResponse


def parse_json_secret(
    secret_name: str, region: str = None, version_stage: str = "AWSCURRENT"
) -> dict:
    request = build_secret_request(
        secret_name=secret_name,
        version_stage=version_stage,
        region=region,
    )
    response = fetch_secret(request)
    return json.loads(response.secret_value)


def get_json_secret_field(
    secret_name: str,
    field_path: str,
    region: str = None,
    default: Any = None,
) -> Any:
    data = parse_json_secret(secret_name, region)
    keys = field_path.split(".")
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current


def parse_json_secret_with_validation(
    secret_name: str,
    required_fields: list[str],
    region: str = None,
) -> tuple[dict, list[str]]:
    data = parse_json_secret(secret_name, region)
    missing = [f for f in required_fields if f not in data]
    return data, missing
