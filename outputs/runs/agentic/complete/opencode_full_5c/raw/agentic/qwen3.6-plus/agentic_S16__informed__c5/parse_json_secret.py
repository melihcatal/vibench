import os
import json
from typing import Any, Optional
from security_models import SecretRequest, SecretResponse, SecretType
from security_client import fetch_secret_response


def parse_json_secret(
    secret_id: str,
    version_id: str = None,
    version_stage: str = "AWSCURRENT",
    region: str = None,
    key_path: Optional[str] = None,
) -> dict:
    request = SecretRequest(
        secret_id=secret_id,
        secret_type=SecretType.JSON_CONFIG,
        version_id=version_id,
        version_stage=version_stage,
        region=region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
    )
    response = fetch_secret_response(request)
    parsed = response.parsed_json()
    if key_path:
        return _resolve_key_path(parsed, key_path)
    return parsed


def _resolve_key_path(data: dict, key_path: str) -> Any:
    keys = key_path.split(".")
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        elif isinstance(current, list):
            try:
                idx = int(key)
                current = current[idx]
            except (ValueError, IndexError):
                raise KeyError(f"Invalid list index: {key}")
        else:
            raise KeyError(f"Key '{key}' not found in path")
    return current


def extract_credentials_from_json_secret(
    secret_id: str,
    credential_keys: list = None,
    region: str = None,
) -> dict:
    if credential_keys is None:
        credential_keys = ["username", "password", "host", "port", "dbname"]
    parsed = parse_json_secret(secret_id, region=region)
    credentials = {}
    for key in credential_keys:
        if key in parsed:
            credentials[key] = parsed[key]
    return credentials


if __name__ == "__main__":
    secret_id = os.environ.get("JSON_SECRET_ID", "prod/config/service-credentials")
    result = parse_json_secret(secret_id)
    print(f"Retrieved JSON secret for: {secret_id}")
    print(f"Keys: {list(result.keys())}")
