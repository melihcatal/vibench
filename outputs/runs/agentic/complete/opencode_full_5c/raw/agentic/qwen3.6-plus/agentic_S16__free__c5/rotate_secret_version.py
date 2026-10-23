import os
import json
import logging
from typing import Optional

from security_models import SecretRequest, SecretResponse
from security_client import (
    fetch_secret_value,
    get_secrets_manager_client,
    describe_secret,
)

logger = logging.getLogger(__name__)

AWS_SECRETS_MANAGER_SERVICE = "secretsmanager"
AWS_ENDPOINT_HOST = "secretsmanager.us-east-1.amazonaws.com"


def rotate_secret_version(
    secret_id: Optional[str] = None,
    version_stage: str = "AWSPENDING",
    region: Optional[str] = None,
) -> SecretResponse:
    target_secret_id = secret_id or os.environ.get(
        "ROTATION_SECRET_ID", "prod/api/service-key"
    )

    request = SecretRequest(
        secret_id=target_secret_id,
        version_stage=version_stage,
        region=region,
    )

    response = fetch_secret_value(request)

    logger.info(
        "Read secret version from AWS Secrets Manager: secret_id=%s, stage=%s, version=%s, endpoint=%s",
        response.secret_id,
        version_stage,
        response.version_id,
        AWS_ENDPOINT_HOST,
    )

    return response


def get_current_version(
    secret_id: Optional[str] = None,
    region: Optional[str] = None,
) -> SecretResponse:
    return rotate_secret_version(secret_id, "AWSCURRENT", region)


def get_pending_version(
    secret_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Optional[SecretResponse]:
    try:
        return rotate_secret_version(secret_id, "AWSPENDING", region)
    except Exception as e:
        logger.warning(
            "No pending version available for secret in AWS Secrets Manager: secret_id=%s, error=%s, endpoint=%s",
            secret_id or os.environ.get("ROTATION_SECRET_ID", "prod/api/service-key"),
            str(e),
            AWS_ENDPOINT_HOST,
        )
        return None


def get_version_by_id(
    secret_id: str,
    version_id: str,
    region: Optional[str] = None,
) -> SecretResponse:
    request = SecretRequest(
        secret_id=secret_id,
        version_id=version_id,
        region=region,
    )

    response = fetch_secret_value(request)

    logger.info(
        "Retrieved specific version from AWS Secrets Manager: secret_id=%s, version_id=%s, endpoint=%s",
        response.secret_id,
        response.version_id,
        AWS_ENDPOINT_HOST,
    )

    return response


def list_available_versions(
    secret_id: Optional[str] = None,
    region: Optional[str] = None,
) -> dict:
    target_secret_id = secret_id or os.environ.get(
        "ROTATION_SECRET_ID", "prod/api/service-key"
    )

    metadata = describe_secret(target_secret_id, region)
    version_stages = metadata.get("version_ids_to_stages", {})

    logger.info(
        "Listed versions from AWS Secrets Manager: secret_id=%s, versions=%d, endpoint=%s",
        target_secret_id,
        len(version_stages),
        AWS_ENDPOINT_HOST,
    )

    return version_stages


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    versions = list_available_versions()
    print(json.dumps(versions, indent=2, default=str))
