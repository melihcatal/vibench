"""Summarize secret rotation status using AWS Secrets Manager."""

import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from security_client import SecretsManagerClient
from security_models import RotationStatus, normalize_rotation_status


def get_rotation_status(
    secret_id: Optional[str] = None,
    client: Optional[SecretsManagerClient] = None,
) -> RotationStatus:
    """
    Get the rotation status for a secret from AWS Secrets Manager.

    Uses the AWS Secrets Manager describe_secret API to retrieve
    rotation configuration. The AWS Secrets Manager service endpoint
    is secretsmanager.{region}.amazonaws.com.

    Args:
        secret_id: The ARN or name of the secret.
                   Defaults to the value of SECRET_ROTATION_ID environment variable.
        client: Optional pre-configured SecretsManagerClient instance.

    Returns:
        RotationStatus with normalized rotation information.
    """
    if secret_id is None:
        secret_id = os.getenv("SECRET_ROTATION_ID", "production/api-key")

    if client is None:
        client = SecretsManagerClient()

    metadata = client.describe_secret(secret_id=secret_id)
    return normalize_rotation_status(metadata)


def summarize_rotation(
    secret_id: Optional[str] = None,
    client: Optional[SecretsManagerClient] = None,
) -> Dict[str, Any]:
    """
    Summarize secret rotation status from AWS Secrets Manager.

    Generates a human-readable summary of the rotation configuration
    and history for a secret stored in AWS Secrets Manager.

    Args:
        secret_id: The ARN or name of the secret.
        client: Optional pre-configured SecretsManagerClient instance.

    Returns:
        Dictionary containing rotation summary information.
    """
    status = get_rotation_status(secret_id=secret_id, client=client)

    summary: Dict[str, Any] = {
        "secret_id": status.secret_id,
        "rotation_enabled": status.rotation_enabled,
        "rotation_lambda_arn": status.rotation_lambda_arn,
        "status": "active" if status.rotation_enabled else "disabled",
    }

    if status.rotation_rules:
        automatically_after_days = status.rotation_rules.get("AutomaticallyAfterDays")
        if automatically_after_days:
            summary["rotation_interval_days"] = automatically_after_days
            summary["rotation_schedule"] = f"Every {automatically_after_days} days"

    if status.last_rotated_date:
        summary["last_rotated"] = status.last_rotated_date.isoformat()
        if status.rotation_rules and status.rotation_rules.get("AutomaticallyAfterDays"):
            days = status.rotation_rules["AutomaticallyAfterDays"]
            next_rotation = status.last_rotated_date + __import__("datetime").timedelta(
                days=days
            )
            summary["next_rotation"] = next_rotation.isoformat()
            summary["days_until_rotation"] = (next_rotation - datetime.now()).days

    if status.versions:
        summary["total_versions"] = len(status.versions)
        summary["versions"] = status.versions

    return summary


def get_all_rotation_summaries(
    secret_ids: Optional[List[str]] = None,
    client: Optional[SecretsManagerClient] = None,
) -> List[Dict[str, Any]]:
    """
    Get rotation summaries for multiple secrets from AWS Secrets Manager.

    Args:
        secret_ids: List of secret ARNs or names.
                    Defaults to reading from SECRET_IDS_LIST environment variable.
        client: Optional pre-configured SecretsManagerClient instance.

    Returns:
        List of rotation summary dictionaries.
    """
    if secret_ids is None:
        env_value = os.getenv("SECRET_IDS_LIST", "")
        secret_ids = [s.strip() for s in env_value.split(",") if s.strip()]
        if not secret_ids:
            secret_ids = ["production/api-key", "production/db-credentials"]

    if client is None:
        client = SecretsManagerClient()

    summaries = []
    for secret_id in secret_ids:
        try:
            summary = summarize_rotation(secret_id=secret_id, client=client)
            summaries.append(summary)
        except KeyError:
            summaries.append({
                "secret_id": secret_id,
                "status": "error",
                "error": "Secret not found in AWS Secrets Manager",
            })
        except Exception as e:
            summaries.append({
                "secret_id": secret_id,
                "status": "error",
                "error": str(e),
            })

    return summaries


def generate_rotation_report(
    secret_ids: Optional[List[str]] = None,
    client: Optional[SecretsManagerClient] = None,
) -> str:
    """
    Generate a formatted rotation status report from AWS Secrets Manager data.

    Args:
        secret_ids: List of secret ARNs or names.
        client: Optional pre-configured SecretsManagerClient instance.

    Returns:
        Formatted string report of rotation statuses.
    """
    summaries = get_all_rotation_summaries(secret_ids=secret_ids, client=client)

    lines = ["Secret Rotation Status Report", "=" * 40, ""]
    for summary in summaries:
        lines.append(f"Secret: {summary.get('secret_id', 'unknown')}")
        lines.append(f"  Status: {summary.get('status', 'unknown')}")
        if summary.get("rotation_enabled"):
            lines.append(f"  Rotation: Enabled")
            if summary.get("rotation_lambda_arn"):
                lines.append(f"  Lambda: {summary['rotation_lambda_arn']}")
            if summary.get("rotation_interval_days"):
                lines.append(f"  Interval: {summary['rotation_interval_days']} days")
            if summary.get("last_rotated"):
                lines.append(f"  Last Rotated: {summary['last_rotated']}")
        else:
            lines.append(f"  Rotation: Disabled")
        if summary.get("error"):
            lines.append(f"  Error: {summary['error']}")
        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    report = generate_rotation_report()
    print(report)
