import boto3
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional
from botocore.exceptions import ClientError


def get_rotation_summary(secret_name: str) -> Dict[str, any]:
    """
    Summarize secret rotation status using AWS Secrets Manager.

    Args:
        secret_name: Name of the secret

    Returns:
        Dictionary with rotation summary
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        # Get secret description
        describe_response = client.describe_secret(SecretId=secret_name)

        # Get current version
        current_response = client.get_secret_value(
            SecretId=secret_name, VersionStage="AWSCURRENT"
        )

        summary = {
            "secret_name": secret_name,
            "arn": describe_response.get("ARN"),
            "rotation_enabled": describe_response.get("RotationEnabled", False),
            "last_rotated_date": describe_response.get("LastRotatedDate"),
            "last_changed_date": describe_response.get("LastChangedDate"),
            "last_accessed_date": describe_response.get("LastAccessedDate"),
            "current_version_id": current_response.get("VersionId"),
            "current_version_stages": current_response.get("VersionStages", []),
            "description": describe_response.get("Description", ""),
            "tags": {
                tag["Key"]: tag["Value"] for tag in describe_response.get("Tags", [])
            },
        }

        # Check for pending version
        try:
            pending_response = client.get_secret_value(
                SecretId=secret_name, VersionStage="AWSPENDING"
            )
            summary["pending_version_id"] = pending_response.get("VersionId")
            summary["pending_exists"] = True
        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceNotFoundException":
                summary["pending_version_id"] = None
                summary["pending_exists"] = False
            else:
                raise

        # Check for previous version
        try:
            previous_response = client.get_secret_value(
                SecretId=secret_name, VersionStage="AWSPREVIOUS"
            )
            summary["previous_version_id"] = previous_response.get("VersionId")
            summary["previous_exists"] = True
        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceNotFoundException":
                summary["previous_version_id"] = None
                summary["previous_exists"] = False
            else:
                raise

        # Calculate rotation metrics
        if summary["rotation_enabled"] and summary["last_rotated_date"]:
            last_rotated = summary["last_rotated_date"]
            now = datetime.now(timezone.utc)
            days_since_rotation = (now - last_rotated).days

            rotation_rules = describe_response.get("RotationRules", {})
            rotation_interval = rotation_rules.get("AutomaticallyAfterDays")

            summary["days_since_last_rotation"] = days_since_rotation
            summary["rotation_interval_days"] = rotation_interval

            if rotation_interval:
                days_until_next = max(0, rotation_interval - days_since_rotation)
                summary["days_until_next_rotation"] = days_until_next
                summary["rotation_due_soon"] = days_until_next <= 7
            else:
                summary["days_until_next_rotation"] = None
                summary["rotation_due_soon"] = False

        # Get version list for additional insights
        try:
            versions_response = client.list_secret_version_ids(SecretId=secret_name)
            versions = versions_response.get("Versions", [])
            summary["total_versions"] = len(versions)

            # Count versions by stage
            stage_counts = {}
            for version in versions:
                for stage in version.get("VersionStages", []):
                    stage_counts[stage] = stage_counts.get(stage, 0) + 1
            summary["version_stage_counts"] = stage_counts

        except ClientError:
            summary["total_versions"] = 0
            summary["version_stage_counts"] = {}

        # Determine rotation status
        if summary["rotation_enabled"]:
            if summary["pending_exists"]:
                summary["rotation_status"] = "PENDING_ROTATION"
            elif summary.get("days_until_next_rotation", 999) <= 0:
                summary["rotation_status"] = "DUE_FOR_ROTATION"
            else:
                summary["rotation_status"] = "ROTATION_ENABLED"
        else:
            summary["rotation_status"] = "ROTATION_DISABLED"

        return summary

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ResourceNotFoundException":
            raise Exception(f"Secret '{secret_name}' not found in AWS Secrets Manager")
        else:
            raise Exception(f"Failed to get rotation summary: {e}")


def format_rotation_summary(summary: Dict[str, any]) -> str:
    """
    Format rotation summary as a readable string.

    Args:
        summary: Rotation summary dictionary

    Returns:
        Formatted summary string
    """
    lines = []
    lines.append(f"Secret: {summary['secret_name']}")
    lines.append(f"Status: {summary['rotation_status']}")
    lines.append(f"Rotation Enabled: {summary['rotation_enabled']}")

    if summary["rotation_enabled"]:
        lines.append(f"Current Version: {summary['current_version_id']}")

        if summary["pending_exists"]:
            lines.append(
                f"Pending Version: {summary['pending_version_id']} (awaiting activation)"
            )

        if summary["previous_exists"]:
            lines.append(f"Previous Version: {summary['previous_version_id']}")

        if "days_since_last_rotation" in summary:
            lines.append(
                f"Days since last rotation: {summary['days_since_last_rotation']}"
            )

        if (
            "days_until_next_rotation" in summary
            and summary["days_until_next_rotation"] is not None
        ):
            lines.append(
                f"Days until next rotation: {summary['days_until_next_rotation']}"
            )

            if summary["rotation_due_soon"]:
                lines.append("⚠️  Rotation due soon!")

    lines.append(f"Total versions: {summary.get('total_versions', 'Unknown')}")

    return "\n".join(lines)


if __name__ == "__main__":
    summary = get_rotation_summary("prod/api-key")
    print(format_rotation_summary(summary))
