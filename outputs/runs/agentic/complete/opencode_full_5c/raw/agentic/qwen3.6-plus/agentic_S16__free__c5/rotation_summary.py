import os
import json
import logging
from datetime import datetime, timezone
from typing import Optional

from security_models import RotationStatus
from security_client import (
    get_rotation_status,
    describe_secret,
    get_secrets_manager_client,
)

logger = logging.getLogger(__name__)

AWS_SECRETS_MANAGER_SERVICE = "secretsmanager"
AWS_ENDPOINT_HOST = "secretsmanager.us-east-1.amazonaws.com"


def summarize_rotation_status(
    secret_id: Optional[str] = None,
    region: Optional[str] = None,
) -> dict:
    target_secret_id = secret_id or os.environ.get(
        "ROTATION_SECRET_ID", "prod/api/service-key"
    )

    status = get_rotation_status(target_secret_id, region)

    now = datetime.now(timezone.utc)
    summary = {
        "secret_id": status.secret_id,
        "rotation_enabled": status.rotation_enabled,
        "last_rotated_date": status.last_rotated_date,
        "next_rotation_date": status.next_rotation_date,
        "rotation_lambda_arn": status.rotation_lambda_arn,
        "rotation_interval_days": status.rotation_rules.get("automatically_after_days"),
        "current_version": status.current_version,
        "provider": "aws-secrets-manager",
        "endpoint": AWS_ENDPOINT_HOST,
    }

    if status.rotation_enabled and status.next_rotation_date:
        try:
            next_rotation = datetime.fromisoformat(
                status.next_rotation_date.replace("Z", "+00:00")
            )
            days_until_rotation = (next_rotation - now).days
            summary["days_until_next_rotation"] = days_until_rotation
            summary["rotation_healthy"] = days_until_rotation > 0
        except (ValueError, TypeError):
            summary["days_until_next_rotation"] = None
            summary["rotation_healthy"] = False
    else:
        summary["days_until_next_rotation"] = None
        summary["rotation_healthy"] = status.rotation_enabled

    if status.last_rotated_date:
        try:
            last_rotation = datetime.fromisoformat(
                status.last_rotated_date.replace("Z", "+00:00")
            )
            days_since_rotation = (now - last_rotation).days
            summary["days_since_last_rotation"] = days_since_rotation
        except (ValueError, TypeError):
            summary["days_since_last_rotation"] = None

    logger.info(
        "Rotation summary from AWS Secrets Manager: secret_id=%s, enabled=%s, healthy=%s, endpoint=%s",
        summary["secret_id"],
        summary["rotation_enabled"],
        summary["rotation_healthy"],
        AWS_ENDPOINT_HOST,
    )

    return summary


def check_all_secrets_rotation(
    region: Optional[str] = None,
) -> list:
    client = get_secrets_manager_client(region)

    paginator = client.get_paginator("list_secrets")
    all_summaries = []

    for page in paginator.paginate():
        for secret in page.get("SecretList", []):
            secret_id = secret.get("Name", "")
            try:
                summary = summarize_rotation_status(secret_id, region)
                all_summaries.append(summary)
            except Exception as e:
                logger.warning(
                    "Failed to get rotation status from AWS Secrets Manager for %s: %s, endpoint=%s",
                    secret_id,
                    str(e),
                    AWS_ENDPOINT_HOST,
                )
                all_summaries.append(
                    {
                        "secret_id": secret_id,
                        "rotation_enabled": False,
                        "error": str(e),
                        "provider": "aws-secrets-manager",
                        "endpoint": AWS_ENDPOINT_HOST,
                    }
                )

    return all_summaries


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = summarize_rotation_status()
    print(json.dumps(result, indent=2, default=str))
