"""
Summarize secret rotation status from AWS Secrets Manager.

This module queries AWS Secrets Manager for rotation configuration
and generates a summary of rotation health for each secret.
"""

import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError

from security_client import get_secrets_manager_client
from security_models import SecretRotationStatus

logger = logging.getLogger(__name__)

AWS_PROVIDER_ID = "aws-secrets-manager"


def get_rotation_status(
    secret_name: str, region_name: str = "us-east-1"
) -> Optional[SecretRotationStatus]:
    """
    Get the rotation status for a secret in AWS Secrets Manager.

    Args:
        secret_name: The secret name or ARN.
        region_name: AWS region.

    Returns:
        SecretRotationStatus or None if retrieval fails.
    """
    try:
        client = get_secrets_manager_client(region_name=region_name)
        response = client.describe_secret(SecretId=secret_name)

        rotation_enabled = response.get("RotationEnabled", False)
        rotation_rules = response.get("RotationRules", {})

        rotation_lambda_arn = response.get("RotationLambdaARN")
        last_rotated = response.get("LastRotatedDate")
        last_changed = response.get("LastChangedDate")
        last_accessed = response.get("LastAccessedDate")

        version_ids = response.get("VersionIdsToStages", {})

        current_version = None
        pending_version = None
        for version_id, stages in version_ids.items():
            if "AWSCURRENT" in stages:
                current_version = version_id
            if "AWSPENDING" in stages:
                pending_version = version_id

        next_rotation_date = None
        if rotation_rules:
            automatically_after_days = rotation_rules.get("AutomaticallyAfterDays")
            if automatically_after_days and last_rotated:
                next_rotation_date = (
                    last_rotated + __import__("datetime").timedelta(
                        days=automatically_after_days
                    )
                ).isoformat()

        return SecretRotationStatus(
            secret_name=secret_name,
            provider=AWS_PROVIDER_ID,
            rotation_enabled=rotation_enabled,
            rotation_lambda_arn=rotation_lambda_arn,
            rotation_rules=rotation_rules,
            last_rotated_date=last_rotated.isoformat() if last_rotated else None,
            next_rotation_date=next_rotation_date,
            current_version_stage=current_version,
            pending_version_stage=pending_version,
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        logger.error(
            "Error getting rotation status for %s from AWS: %s",
            secret_name,
            error_code,
        )
        return None


def summarize_all_rotations(
    secret_names: List[str], region_name: str = "us-east-1"
) -> Dict[str, Any]:
    """
    Generate a summary of rotation status for multiple secrets.

    Args:
        secret_names: List of secret names or ARNs.
        region_name: AWS region.

    Returns:
        Dictionary with rotation summary including health score.
    """
    statuses = []
    for name in secret_names:
        status = get_rotation_status(name, region_name)
        if status:
            statuses.append(status)

    total = len(statuses)
    enabled = sum(1 for s in statuses if s.rotation_enabled)
    has_pending = sum(1 for s in statuses if s.pending_version_stage)

    health_score = (enabled / total * 100) if total > 0 else 0

    summary = {
        "provider": AWS_PROVIDER_ID,
        "total_secrets": total,
        "rotation_enabled_count": enabled,
        "rotation_disabled_count": total - enabled,
        "pending_rotation_count": has_pending,
        "health_score": round(health_score, 2),
        "secrets": [
            {
                "name": s.secret_name,
                "rotation_enabled": s.rotation_enabled,
                "last_rotated": s.last_rotated_date,
                "next_rotation": s.next_rotation_date,
                "has_pending_version": bool(s.pending_version_stage),
            }
            for s in statuses
        ],
    }

    return summary
