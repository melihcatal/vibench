import os
import json
import logging
from typing import Optional, Any

from security_models import SecretRequest, SecretResponse, ParsedSecret
from security_client import fetch_secret_value, get_secrets_manager_client

logger = logging.getLogger(__name__)

AWS_SECRETS_MANAGER_SERVICE = "secretsmanager"
AWS_ENDPOINT_HOST = "secretsmanager.us-east-1.amazonaws.com"


def parse_json_secret(
    secret_id: Optional[str] = None,
    version_stage: str = "AWSCURRENT",
    region: Optional[str] = None,
) -> ParsedSecret:
    target_secret_id = secret_id or os.environ.get(
        "JSON_SECRET_ID", "prod/config/application-settings"
    )

    request = SecretRequest(
        secret_id=target_secret_id,
        version_stage=version_stage,
        region=region,
    )

    response = fetch_secret_value(request)
    raw_value = response.secret_value

    try:
        parsed_data = json.loads(raw_value)
    except json.JSONDecodeError as e:
        logger.error(
            "Failed to parse JSON secret from AWS Secrets Manager: secret_id=%s, error=%s, endpoint=%s",
            target_secret_id,
            str(e),
            AWS_ENDPOINT_HOST,
        )
        raise ValueError(f"Secret {target_secret_id} is not valid JSON: {e}")

    parsed_secret = ParsedSecret(
        secret_id=response.secret_id,
        parsed_data=parsed_data,
        raw_value=raw_value,
        version_id=response.version_id,
    )

    logger.info(
        "Successfully parsed JSON secret from AWS Secrets Manager: secret_id=%s, keys=%s, endpoint=%s",
        parsed_secret.secret_id,
        list(parsed_data.keys()) if isinstance(parsed_data, dict) else "non-dict",
        AWS_ENDPOINT_HOST,
    )

    return parsed_secret


def get_json_secret_field(
    field_name: str,
    secret_id: Optional[str] = None,
    version_stage: str = "AWSCURRENT",
    region: Optional[str] = None,
    default: Any = None,
) -> Any:
    parsed = parse_json_secret(secret_id, version_stage, region)

    if not isinstance(parsed.parsed_data, dict):
        return default

    return parsed.parsed_data.get(field_name, default)


def get_nested_json_field(
    field_path: str,
    secret_id: Optional[str] = None,
    version_stage: str = "AWSCURRENT",
    region: Optional[str] = None,
    default: Any = None,
    separator: str = ".",
) -> Any:
    parsed = parse_json_secret(secret_id, version_stage, region)

    if not isinstance(parsed.parsed_data, dict):
        return default

    keys = field_path.split(separator)
    current = parsed.parsed_data

    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default

    return current


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = parse_json_secret()
    print(json.dumps(result.to_dict(), indent=2, default=str))
