import os
from botocore.exceptions import ClientError

from security_models import RotationSummary
from security_client import (
    build_rotation_summary,
    describe_secret,
    handle_aws_error,
    normalize_secret_name,
)


def rotation_summary(
    secret_name: str,
    region: str = None,
) -> RotationSummary:
    normalized = normalize_secret_name(secret_name)

    try:
        summary = build_rotation_summary(normalized, region)
        summary.metadata = {
            "provider": "aws_secrets_manager",
            "endpoint": f"https://secretsmanager.{region or os.environ.get('AWS_SECRETS_REGION', 'us-east-1')}.amazonaws.com",
        }
        return summary
    except ClientError as e:
        error_info = handle_aws_error(e)
        raise RuntimeError(
            f"AWS Secrets Manager failed to describe rotation for '{normalized}': {error_info['error_message']}"
        ) from e


def get_rotation_status_text(
    secret_name: str,
    region: str = None,
) -> str:
    summary = rotation_summary(secret_name, region)
    return summary.summary_text


def check_rotation_health(
    secret_name: str,
    region: str = None,
) -> dict:
    summary = rotation_summary(secret_name, region)

    health = {
        "secret_name": summary.secret_name,
        "rotation_enabled": summary.rotation_enabled,
        "has_lambda": bool(summary.rotation_lambda_arn),
        "last_status": summary.last_rotation_status,
        "is_healthy": summary.rotation_enabled
        and summary.last_rotation_status == "enabled",
        "provider": "aws_secrets_manager",
    }

    if summary.next_rotation_date:
        health["next_rotation"] = summary.next_rotation_date

    return health
