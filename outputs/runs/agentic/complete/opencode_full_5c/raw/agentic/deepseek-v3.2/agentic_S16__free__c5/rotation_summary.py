import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
import boto3
from botocore.exceptions import ClientError
from security_models import RotationStatus, SecretPriority, RotationResult


def rotation_summary(secret_names: List[str] = None) -> Dict[str, Any]:
    """
    Summarize secret rotation status from AWS Secrets Manager.

    Args:
        secret_names: List of secret names to check (None for all secrets)

    Returns:
        Dictionary with rotation summary
    """
    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    summary = {
        "total_secrets": 0,
        "rotation_enabled": 0,
        "rotation_disabled": 0,
        "rotation_failed": 0,
        "rotation_pending": 0,
        "secrets": [],
        "critical_secrets": [],
        "rotation_schedule": {"next_24_hours": 0, "next_7_days": 0, "overdue": 0},
        "last_updated": datetime.utcnow().isoformat(),
    }

    try:
        # Get list of secrets
        if secret_names:
            secrets_to_check = []
            for name in secret_names:
                try:
                    response = client.describe_secret(SecretId=name)
                    secrets_to_check.append(response)
                except ClientError as e:
                    if e.response["Error"]["Code"] == "ResourceNotFoundException":
                        print(f"Warning: Secret {name} not found")
                    continue
        else:
            # Get all secrets (paginated)
            secrets_to_check = []
            paginator = client.get_paginator("list_secrets")
            for page in paginator.paginate():
                secrets_to_check.extend(page["SecretList"])

        summary["total_secrets"] = len(secrets_to_check)

        for secret_info in secrets_to_check:
            secret_name = secret_info["Name"]
            rotation_enabled = secret_info.get("RotationEnabled", False)
            rotation_rules = secret_info.get("RotationRules")
            last_rotated = secret_info.get("LastRotatedDate")
            last_changed = secret_info.get("LastChangedDate")

            # Determine rotation status
            rotation_status = RotationStatus.DISABLED
            next_rotation = None
            is_overdue = False

            if rotation_enabled and rotation_rules:
                rotation_status = RotationStatus.ACTIVE
                automatically_after_days = rotation_rules.get("AutomaticallyAfterDays")

                if last_rotated and automatically_after_days:
                    next_rotation_date = last_rotated + timedelta(
                        days=automatically_after_days
                    )
                    next_rotation = next_rotation_date.isoformat()

                    if datetime.utcnow() > next_rotation_date:
                        rotation_status = RotationStatus.OVERDUE
                        is_overdue = True
                        summary["rotation_schedule"]["overdue"] += 1
                    elif datetime.utcnow() + timedelta(hours=24) > next_rotation_date:
                        summary["rotation_schedule"]["next_24_hours"] += 1
                        rotation_status = RotationStatus.SCHEDULED
                    elif datetime.utcnow() + timedelta(days=7) > next_rotation_date:
                        summary["rotation_schedule"]["next_7_days"] += 1
                        rotation_status = RotationStatus.SCHEDULED

            # Determine priority
            priority = SecretPriority.LOW
            tags = secret_info.get("Tags", [])
            for tag in tags:
                if tag["Key"].lower() == "priority":
                    try:
                        priority = SecretPriority(tag["Value"].lower())
                    except ValueError:
                        pass
                elif (
                    tag["Key"].lower() == "critical" and tag["Value"].lower() == "true"
                ):
                    priority = SecretPriority.CRITICAL

            if priority == SecretPriority.CRITICAL:
                summary["critical_secrets"].append(secret_name)

            # Check for rotation failures
            rotation_failed = False
            if rotation_enabled:
                try:
                    rotation_status_response = client.describe_secret(
                        SecretId=secret_name
                    )
                    if rotation_status_response.get("RotationLastFailedTime"):
                        rotation_status = RotationStatus.FAILED
                        rotation_failed = True
                        summary["rotation_failed"] += 1
                except ClientError:
                    pass

            # Update counters
            if rotation_enabled:
                if rotation_failed:
                    summary["rotation_failed"] += 1
                elif rotation_status == RotationStatus.OVERDUE:
                    summary["rotation_pending"] += 1
                else:
                    summary["rotation_enabled"] += 1
            else:
                summary["rotation_disabled"] += 1

            # Add secret details
            secret_details = {
                "name": secret_name,
                "arn": secret_info.get("ARN"),
                "rotation_enabled": rotation_enabled,
                "rotation_status": rotation_status.value,
                "priority": priority.value,
                "last_rotated": last_rotated.isoformat() if last_rotated else None,
                "last_changed": last_changed.isoformat() if last_changed else None,
                "next_rotation": next_rotation,
                "is_overdue": is_overdue,
                "tags": {tag["Key"]: tag["Value"] for tag in tags},
            }

            if rotation_rules:
                secret_details["rotation_rules"] = rotation_rules

            summary["secrets"].append(secret_details)

        # Calculate percentages
        if summary["total_secrets"] > 0:
            summary["rotation_enabled_percent"] = round(
                (summary["rotation_enabled"] / summary["total_secrets"]) * 100, 1
            )
            summary["rotation_disabled_percent"] = round(
                (summary["rotation_disabled"] / summary["total_secrets"]) * 100, 1
            )
            summary["rotation_failed_percent"] = round(
                (summary["rotation_failed"] / summary["total_secrets"]) * 100, 1
            )
            summary["rotation_pending_percent"] = round(
                (summary["rotation_pending"] / summary["total_secrets"]) * 100, 1
            )

        # Generate recommendations
        recommendations = []
        if summary["rotation_schedule"]["overdue"] > 0:
            recommendations.append(
                f"{summary['rotation_schedule']['overdue']} secrets are overdue for rotation"
            )
        if summary["rotation_failed"] > 0:
            recommendations.append(
                f"{summary['rotation_failed']} secrets have failed rotations that need attention"
            )
        if summary["rotation_disabled"] > len(summary["critical_secrets"]):
            recommendations.append(
                f"Consider enabling rotation for {summary['rotation_disabled'] - len(summary['critical_secrets'])} non-critical secrets"
            )

        summary["recommendations"] = recommendations

        return summary

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "AccessDeniedException":
            raise PermissionError("Access denied to AWS Secrets Manager") from e
        else:
            raise RuntimeError(f"Error fetching rotation summary: {e}") from e
