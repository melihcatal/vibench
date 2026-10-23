import os
import json
from security_client import fetch_secret, parse_json_secret_value
from security_models import SecretRequest, SecretResponse


def parse_json_secret(secret_id: str = None, version_stage: str = "AWSCURRENT") -> dict:
    target_id = secret_id or os.environ.get(
        "JSON_SECRET_ID", "prod/config/app-settings"
    )
    request = SecretRequest(
        secret_id=target_id,
        version_stage=version_stage,
        with_decryption=True,
    )
    return parse_json_secret_value(request)


def get_nested_secret_value(
    secret_id: str, key_path: str, version_stage: str = "AWSCURRENT"
) -> any:
    data = parse_json_secret(secret_id, version_stage)
    keys = key_path.split(".")
    current = data
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key)
        elif isinstance(current, list):
            try:
                current = current[int(key)]
            except (ValueError, IndexError):
                return None
        else:
            return None
    return current


def flatten_json_secret(
    secret_id: str, version_stage: str = "AWSCURRENT", prefix: str = ""
) -> dict:
    data = parse_json_secret(secret_id, version_stage)
    flattened = {}

    def _flatten(obj, parent_key=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                new_key = f"{parent_key}.{k}" if parent_key else k
                _flatten(v, new_key)
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                new_key = f"{parent_key}.{i}" if parent_key else str(i)
                _flatten(v, new_key)
        else:
            flattened[parent_key] = obj

    _flatten(data, prefix)
    return flattened


def validate_json_secret_schema(
    secret_id: str, required_keys: list, version_stage: str = "AWSCURRENT"
) -> dict:
    data = parse_json_secret(secret_id, version_stage)
    missing = [k for k in required_keys if k not in data]
    return {
        "valid": len(missing) == 0,
        "missing_keys": missing,
        "present_keys": list(data.keys()),
        "secret_id": secret_id,
    }


if __name__ == "__main__":
    result = parse_json_secret()
    print(json.dumps(result, indent=2, default=str))
