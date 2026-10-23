"""Summarize secret rotation status using AWS Secrets Manager metadata."""

import os
import json
from datetime import datetime
from typing import Optional
import boto3
from botocore.exceptions import ClientError
from security_client import get_secrets_client
from security_models import RotationStatus, SecretError


def fetch_rotation_status(secret_id: str, region: str = None) -> RotationStatus:
    """Fetch rotation status for a secret from AWS Secrets Manager.

    Uses the describe_secret API to retrieve rotation metadata including
    rotation Lambda ARN, rotation rules, and version staging information.

    Args:
        secret_id: The name or ARN of the secret.
        region: AWS region override.

    Returns:
        RotationStatus with normalized rotation metadata from AWS Secrets Manager.
    """
    try:
        client = get_secrets_client(region=region)
        response = client.describe_secret(SecretId=secret_id)
        versions = response.get("VersionIdsToStages", {})

        current_version = ""
        pending_version = ""
        for vid, stages in versions.items():
            if "AWSCURRENT" in stages:
                current_version = vid
            if "AWSPENDING" in stages:
                pending_version = vid

        rotation_rules = response.get("RotationRules", {})
        last_rotated = response.get("LastRotatedDate")
        next_rotation = response.get("NextRotationDate")

        return RotationStatus(
            secret_id=secret_id,
            rotation_enabled=response.get("RotationEnabled", False),
            rotation_lambda_arn=response.get("RotationLambdaARN", ""),
            rotation_rules={
                "automatically_after_days": rotation_rules.get("AutomaticallyAfterDays"),
                "duration": rotation_rules.get("Duration"),
            },
            last_rotated_date=last_rotated,
            next_rotation_date=next_rotation,
            current_version=current_version,
            pending_version=pending_version,
            provider="aws_secrets_manager",
        )
    except ClientError as exc:
        error_code = exc.response["Error"]["Code"]
        raise SecretError(
            secret_id=secret_id,
            message=f"AWS Secrets Manager error: {error_code}",
            error_code=error_code,
        )


def summarize_rotation(secret_ids: list[str], region: str = None) -> list[dict]:
    """Summarize rotation status for multiple secrets from AWS Secrets Manager.

    Returns a list of summary dicts suitable for reporting or dashboards.
    """
    summaries = []
    for secret_id in secret_ids:
        try:
            status = fetch_rotation_status(secret_id, region=region)
            summaries.append(
                {
                    "secret_id": status.secret_id,
                    "rotation_enabled": status.rotation_enabled,
                    "rotation_lambda": status.rotation_lambda_arn,
                    "auto_rotate_days": status.rotation_rules.get("automatically_after_days"),
                    "current_version": status.current_version,
                    "pending_version": status.pending_version,
                    "has_pending_rotation": bool(status.pending_version),
                    "provider": "aws_secrets_manager",
                }
            )
        except SecretError as exc:
            summaries.append(
                {
                    "secret_id": secret_id,
                    "rotation_enabled": False,
                    "error": str(exc),
                    "provider": "aws_secrets_manager",
                }
            )
    return summaries


def format_rotation_report(secret_ids: list[str], region: str = None) -> str:
    """Format a human-readable rotation status report from AWS Secrets Manager data."""
    summaries = summarize_rotation(secret_ids, region=region)
    lines = ["=== AWS Secrets Manager Rotation Status Report ===", ""]
    for s in summaries:
        enabled_str = "ENABLED" if s.get("rotation_enabled") else "DISABLED"
        lines.append(f"Secret: {s['secret_id']}")
        lines.append(f"  Rotation: {enabled_str}")
        if s.get("rotation_lambda"):
            lines.append(f"  Lambda ARN: {s['rotation_lambda']}")
        if s.get("auto_rotate_days"):
            lines.append(f"  Auto-rotate: every {s['auto_rotate_days']} days")
        if s.get("pending_version"):
            lines.append(f"  PENDING rotation in progress: {s['pending_version']}")
        if s.get("error"):
            lines.append(f"  ERROR: {s['error']}")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    secrets_list = os.environ.get(
        "SECRET_IDS", "prod/api/key,prod/database/primary"
    ).split(",")
    report = format_rotation_report(secrets_list)
    print(report)
