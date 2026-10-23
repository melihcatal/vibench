"""Summarize secret rotation status using AWS Secrets Manager metadata.

Provider: AWS Secrets Manager (boto3)
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

import os
import json
import boto3
from botocore.exceptions import ClientError

from security_client import get_secret_manager_client, resolve_secret_name


def summarize_rotation_status(secret_name: str | None = None) -> dict:
    """Summarize the rotation status for a secret in AWS Secrets Manager.

    Returns a structured summary including:
      - last rotation date
      - rotation enabled/disabled
      - current and pending version stages
      - rotation rule details
    """
    target_name = resolve_secret_name(secret_name, default_env="ROTATABLE_SECRET_NAME")
    client = get_secret_manager_client()

    try:
        describe_response = client.describe_secret(SecretId=target_name)

        rotation_enabled = describe_response.get("RotationEnabled", False)
        rotation_rules = describe_response.get("RotationRules", {})
        version_ids_to_stages = describe_response.get("VersionIdsToStages", {})

        current_versions = [
            vid for vid, stages in version_ids_to_stages.items()
            if "AWSCURRENT" in stages
        ]
        pending_versions = [
            vid for vid, stages in version_ids_to_stages.items()
            if "AWSPENDING" in stages
        ]

        summary = {
            "secret_name": target_name,
            "rotation_enabled": rotation_enabled,
            "rotation_interval_days": rotation_rules.get("AutomaticallyAfterDays"),
            "current_versions": current_versions,
            "pending_versions": pending_versions,
            "last_rotation_date": describe_response.get("LastRotatedDate"),
            "last_changed_date": describe_response.get("LastChangedDate"),
            "provider": "aws_secrets_manager",
        }

        return summary

    except ClientError as exc:
        return {
            "secret_name": target_name,
            "error": f"AWS Secrets Manager error: {exc.response['Error']['Code']}",
            "provider": "aws_secrets_manager",
        }


def format_summary(summary: dict) -> str:
    """Format the rotation summary for display."""
    lines = [
        f"Secret: {summary.get('secret_name')}",
        f"Provider: {summary.get('provider')}",
        f"Rotation Enabled: {summary.get('rotation_enabled', False)}",
        f"Rotation Interval: {summary.get('rotation_interval_days', 'N/A')} days",
        f"Current Versions: {', '.join(summary.get('current_versions', [])) or 'none'}",
        f"Pending Versions: {', '.join(summary.get('pending_versions', [])) or 'none'}",
        f"Last Rotated: {summary.get('last_rotation_date', 'N/A')}",
    ]
    if summary.get("error"):
        lines.append(f"Error: {summary['error']}")
    return "\n".join(lines)


if __name__ == "__main__":
    summary = summarize_rotation_status()
    print(format_summary(summary))
