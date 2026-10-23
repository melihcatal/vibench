import os
import boto3
from datetime import datetime, timezone
from typing import Dict, List, Optional
from botocore.exceptions import ClientError


def rotation_summary(secret_name: str) -> Dict[str, any]:
    """
    Summarize secret rotation status from AWS Secrets Manager.

    Args:
        secret_name: Name of the secret in AWS Secrets Manager

    Returns:
        Dictionary with rotation summary
    """
    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    try:
        # Get secret details
        secret_details = client.describe_secret(SecretId=secret_name)

        # Get rotation configuration
        rotation_enabled = secret_details.get("RotationEnabled", False)
        rotation_lambda_arn = secret_details.get("RotationLambdaARN")
        rotation_rules = secret_details.get("RotationRules", {})

        # Get secret versions
        versions_response = client.list_secret_version_ids(SecretId=secret_name)
        versions = versions_response.get("Versions", [])

        # Organize versions by stage
        stages = {}
        current_version = None
        pending_version = None
        previous_version = None

        for version in versions:
            version_id = version.get("VersionId")
            version_stages = version.get("VersionStages", [])

            for stage in version_stages:
                if stage not in stages:
                    stages[stage] = []
                stages[stage].append(version_id)

            # Identify special stages
            if "AWSCURRENT" in version_stages:
                current_version = version_id
            if "AWSPENDING" in version_stages:
                pending_version = version_id
            if "AWSPREVIOUS" in version_stages:
                previous_version = version_id

        # Calculate rotation statistics
        total_versions = len(versions)
        rotated_versions = sum(
            1 for v in versions if "AWSPREVIOUS" in v.get("VersionStages", [])
        )

        # Get last rotated date
        last_rotated_date = None
        if previous_version:
            prev_version = next(
                (v for v in versions if v.get("VersionId") == previous_version), None
            )
            if prev_version:
                last_rotated_date = prev_version.get(
                    "LastAccessedDate"
                ) or prev_version.get("CreatedDate")

        # Calculate next rotation if enabled
        next_rotation_date = None
        if rotation_enabled and rotation_rules:
            automatically_after_days = rotation_rules.get("AutomaticallyAfterDays")
            if automatically_after_days and last_rotated_date:
                if isinstance(last_rotated_date, datetime):
                    next_rotation_date = last_rotated_date + timedelta(
                        days=automatically_after_days
                    )
                else:
                    # Handle string timestamp
                    last_dt = datetime.fromisoformat(
                        last_rotated_date.replace("Z", "+00:00")
                    )
                    next_rotation_date = last_dt + timedelta(
                        days=automatically_after_days
                    )

        # Build summary
        summary = {
            "secret_name": secret_name,
            "arn": secret_details.get("ARN"),
            "rotation_enabled": rotation_enabled,
            "rotation_configuration": {
                "lambda_arn": rotation_lambda_arn,
                "rules": rotation_rules,
            },
            "versions": {
                "total": total_versions,
                "rotated": rotated_versions,
                "current": current_version,
                "pending": pending_version,
                "previous": previous_version,
            },
            "stages": stages,
            "last_rotated": last_rotated_date.isoformat()
            if isinstance(last_rotated_date, datetime)
            else last_rotated_date,
            "next_rotation": next_rotation_date.isoformat()
            if isinstance(next_rotation_date, datetime)
            else next_rotation_date,
            "created_date": secret_details.get("CreatedDate"),
            "last_accessed_date": secret_details.get("LastAccessedDate"),
            "tags": secret_details.get("Tags", []),
        }

        return summary

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ResourceNotFoundException":
            raise ValueError(f"Secret {secret_name} not found") from e
        else:
            raise RuntimeError(
                f"Error getting rotation summary for {secret_name}: {e}"
            ) from e
