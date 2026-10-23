import os
import boto3
from botocore.exceptions import ClientError
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta


def rotation_summary(secret_names: List[str]) -> Dict[str, Any]:
    """
    Summarize secret rotation status from AWS Secrets Manager.

    Args:
        secret_names: List of secret names to check

    Returns:
        Dictionary with rotation summary for each secret
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    summary = {
        "total_secrets": len(secret_names),
        "rotation_enabled": 0,
        "rotation_disabled": 0,
        "rotation_failed": 0,
        "secrets": [],
        "summary_by_status": {},
    }

    for secret_name in secret_names:
        try:
            response = client.describe_secret(SecretId=secret_name)

            rotation_enabled = response.get("RotationEnabled", False)
            last_rotated_date = response.get("LastRotatedDate")
            rotation_rules = response.get("RotationRules", {})
            rotation_lambda_arn = response.get("RotationLambdaARN")

            if rotation_enabled:
                summary["rotation_enabled"] += 1
                status = "enabled"

                if last_rotated_date:
                    days_since_rotation = (
                        datetime.now(last_rotated_date.tzinfo) - last_rotated_date
                    ).days
                    rotation_interval = rotation_rules.get("AutomaticallyAfterDays", 0)

                    if rotation_interval > 0:
                        if days_since_rotation > rotation_interval:
                            status = "overdue"
                            summary["rotation_failed"] += 1
                        elif days_since_rotation > rotation_interval * 0.8:
                            status = "due_soon"
                    else:
                        status = "enabled_no_schedule"
            else:
                summary["rotation_disabled"] += 1
                status = "disabled"

            secret_info = {
                "name": secret_name,
                "arn": response.get("ARN", ""),
                "rotation_enabled": rotation_enabled,
                "status": status,
                "last_rotated_date": last_rotated_date.isoformat()
                if last_rotated_date
                else None,
                "rotation_interval_days": rotation_rules.get(
                    "AutomaticallyAfterDays", 0
                ),
                "rotation_lambda_arn": rotation_lambda_arn,
                "created_date": response.get("CreatedDate").isoformat()
                if response.get("CreatedDate")
                else None,
                "last_changed_date": response.get("LastChangedDate").isoformat()
                if response.get("LastChangedDate")
                else None,
            }

            summary["secrets"].append(secret_info)

            if status not in summary["summary_by_status"]:
                summary["summary_by_status"][status] = 0
            summary["summary_by_status"][status] += 1

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "ResourceNotFoundException":
                secret_info = {
                    "name": secret_name,
                    "error": "not_found",
                    "status": "error",
                }
            else:
                secret_info = {
                    "name": secret_name,
                    "error": error_code,
                    "status": "error",
                }

            summary["secrets"].append(secret_info)

            if "error" not in summary["summary_by_status"]:
                summary["summary_by_status"]["error"] = 0
            summary["summary_by_status"]["error"] += 1

    summary["success_rate"] = (
        (len(secret_names) - summary["summary_by_status"].get("error", 0))
        / len(secret_names)
        if secret_names
        else 0
    )

    return summary
