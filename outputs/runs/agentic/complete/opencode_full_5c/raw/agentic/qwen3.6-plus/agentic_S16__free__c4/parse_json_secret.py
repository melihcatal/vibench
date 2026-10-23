import os
import json
from security_client import create_secrets_manager_client, get_secret_value
from security_models import (
    SecretResponse,
    build_aws_secret_request,
    normalize_secret_payload,
)


def parse_json_secret(secret_id: str, region: str = None) -> dict:
    request = build_aws_secret_request(secret_id, region=region)
    client = create_secrets_manager_client(region=request.region)
    aws_response = get_secret_value(
        client,
        secret_id=request.secret_id,
        version_stage="AWSCURRENT",
    )
    response = SecretResponse.from_aws_response(request.secret_id, aws_response)
    parsed = normalize_secret_payload(response.secret_value)
    return {
        "secret_id": response.secret_id,
        "version_id": response.version_id,
        "parsed_value": parsed,
        "metadata": response.metadata,
    }


def parse_json_secret_field(secret_id: str, field_name: str, region: str = None) -> any:
    result = parse_json_secret(secret_id, region=region)
    parsed_value = result["parsed_value"]
    if not isinstance(parsed_value, dict):
        raise ValueError(
            f"Secret {secret_id} does not contain a JSON object, cannot extract field '{field_name}'"
        )
    if field_name not in parsed_value:
        raise KeyError(f"Field '{field_name}' not found in secret {secret_id}")
    return parsed_value[field_name]


def parse_json_secret_version(
    secret_id: str, version_id: str, region: str = None
) -> dict:
    request = build_aws_secret_request(secret_id, version_id=version_id, region=region)
    client = create_secrets_manager_client(region=request.region)
    aws_response = get_secret_value(
        client,
        secret_id=request.secret_id,
        version_id=request.version_id,
    )
    response = SecretResponse.from_aws_response(request.secret_id, aws_response)
    parsed = normalize_secret_payload(response.secret_value)
    return {
        "secret_id": response.secret_id,
        "version_id": response.version_id,
        "version_stage": response.version_stage,
        "parsed_value": parsed,
        "metadata": response.metadata,
    }


if __name__ == "__main__":
    json_secret_id = os.environ.get("JSON_SECRET_ID", "prod/config/service-credentials")
    result = parse_json_secret(json_secret_id)
    print(json.dumps(result, indent=2, default=str))
