"""
rotation_summary.py - Summarize secret rotation status using AWS Secrets Manager.

Queries secretsmanager.amazonaws.com for rotation configuration, version history,
and produces a structured summary of rotation readiness and compliance status.
"""

from __future__ import annotations

import logging
from typing import Optional, Dict, Any, List

from security_client import (
    get_secretsmanager_client,
    describe_secret,
    list_secret_versions,
)
from security_models import RotationStatus, SecretVersionInfo

logger = logging.getLogger(__name__)


def summarize_rotation_status(
    secret_name: str,
    region: Optional[str] = None,
) -> RotationStatus:
    """
    Summarize the rotation status for a given secret.

    Fetches metadata and version information from AWS Secrets Manager
    to determine if rotation is configured, when it last ran, and what
    versions exist.

    Args:
        secret_name: The name or ARN of the secret.
        region: AWS region override.

    Returns:
        RotationStatus with rotation summary details.
    """
    client = get_secretsmanager_client(region_name=region)
    logger.info("Summarizing rotation status for %s via AWS Secrets Manager", secret_name)

    metadata = describe_secret(client, secret_name)

    rotation_enabled = metadata.get("RotationEnabled", False)
    rotation_lambda = metadata.get("RotationLambdaARN")
    last_rotated = metadata.get("LastRotatedDate")
    rotation_rules = metadata.get("RotationRules", {})
    auto_days = rotation_rules.get("AutomaticallyAfterDays")

    versions_resp = list_secret_versions(client, secret_name)
    versions = versions_resp.get("Versions", [])

    staged_versions: Dict[str, List[str]] = {}
    current_version = ""
    for v in versions:
        vid = v.get("VersionId", "")
        stages = v.get("VersionStages", [])
        staged_versions[vid] = stages
        if "AWSCURRENT" in stages:
            current_version = vid

    status = RotationStatus(
        secret_name=metadata.get("Name", secret_name),
        arn=metadata.get("ARN", ""),
        rotation_enabled=rotation_enabled,
        rotation_lambda_arn=rotation_lambda,
        last_rotated_date=str(last_rotated) if last_rotated else None,
        next_rotation_date=None,
        automatic_rotation_days=auto_days,
        current_version=current_version,
        staged_versions=staged_versions,
    )

    logger.info(
        "Rotation summary: enabled=%s, lambda=%s, versions=%d",
        rotation_enabled,
        rotation_lambda or "none",
        len(versions),
    )
    return status


def check_rotation_compliance(
    secret_name: str,
    max_age_days: int = 90,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Check if a secret's rotation is compliant with a maximum age policy.

    Args:
        secret_name: The name or ARN of the secret.
        max_age_days: Maximum allowed days since last rotation.
        region: AWS region override.

    Returns:
        Dict with compliance status, days since rotation, and recommendations.
    """
    status = summarize_rotation_status(secret_name, region=region)

    from datetime import datetime, timezone

    compliant = True
    days_since_rotation = None
    recommendation = "Rotation is compliant."

    if not status.rotation_enabled:
        compliant = False
        recommendation = f"Enable automatic rotation for {secret_name}."
    elif status.last_rotated_date:
        last_rotated = datetime.fromisoformat(status.last_rotated_date)
        if last_rotated.tzinfo is None:
            last_rotated = last_rotated.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        days_since_rotation = (now - last_rotated).days
        if days_since_rotation > max_age_days:
            compliant = False
            recommendation = f"Secret is {days_since_rotation} days old (max {max_age_days}). Rotate immediately."

    return {
        "secret_name": secret_name,
        "compliant": compliant,
        "days_since_rotation": days_since_rotation,
        "max_age_days": max_age_days,
        "rotation_enabled": status.rotation_enabled,
        "recommendation": recommendation,
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    secret_name = "production/api/stripe-key"
    status = summarize_rotation_status(secret_name)
    print(f"Secret: {status.secret_name}")
    print(f"Rotation enabled: {status.rotation_enabled}")
    print(f"Current version: {status.current_version}")
    print(f"Total versions: {len(status.staged_versions)}")
