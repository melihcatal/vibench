import json
from security_client import build_secrets_manager_client, parse_secret_value
from security_models import (
    SecretRequest,
    SecretResponse,
    normalize_secret_response,
    build_secret_request,
)


def parse_json_secret(secret_id: str, version_stage: str = "AWSCURRENT") -> dict:
    client = build_secrets_manager_client()
    request = build_secret_request(secret_id, version_stage)

    params = {
        "SecretId": request.secret_id,
        "VersionStage": request.version_stage,
    }

    response = client.get_secret_value(**params)
    raw_value = response.get("SecretString", "")
    parsed = parse_secret_value(secret_string=raw_value)
    return parsed


if __name__ == "__main__":
    result = parse_json_secret("production/app-config")
    print(json.dumps(result, indent=2))
