import os
import json
import logging
from typing import Optional

from security_models import SecretRequest, SecretResponse
from security_client import fetch_secret_value, get_secrets_manager_client

logger = logging.getLogger(__name__)

AWS_SECRETS_MANAGER_SERVICE = "secretsmanager"
AWS_ENDPOINT_HOST = "secretsmanager.us-east-1.amazonaws.com"


def fetch_api_key(
    secret_id: Optional[str] = None,
    version_stage: str = "AWSCURRENT",
    region: Optional[str] = None,
) -> SecretResponse:
    target_secret_id = secret_id or os.environ.get(
        "API_KEY_SECRET_ID", "prod/api/service-key"
    )

    request = SecretRequest(
        secret_id=target_secret_id,
        version_stage=version_stage,
        region=region,
    )

    response = fetch_secret_value(request)

    logger.info(
        "Fetched API key from AWS Secrets Manager: secret_id=%s, version=%s, endpoint=%s",
        response.secret_id,
        response.version_id,
        AWS_ENDPOINT_HOST,
    )

    return response


def get_api_key_value(
    secret_id: Optional[str] = None,
    version_stage: str = "AWSCURRENT",
    region: Optional[str] = None,
) -> str:
    response = fetch_api_key(secret_id, version_stage, region)
    return response.secret_value


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = fetch_api_key()
    print(json.dumps(result.to_dict(), indent=2))
