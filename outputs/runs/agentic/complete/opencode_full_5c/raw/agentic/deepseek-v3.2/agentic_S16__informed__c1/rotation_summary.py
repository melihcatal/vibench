import os
import boto3
from botocore.exceptions import ClientError
from typing import List, Dict, Any
from datetime import datetime


def summarize_rotation_status(secret_names: List[str]) -> Dict[str, Any]:
    """
    Summarize secret rotation status using AWS Secrets Manager.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    summary = {
        "total_secrets": len(secret_names),
        "rotation_enabled": 0,
        "rotation_disabled": 0,
        "secrets": [],
        "summary_by_status": {},
    }

    for secret_name in secret_names:
        try:
            response = client.describe_secret(SecretId=secret_name)

            secret_info = {
                "name": secret_name,
                "rotation_enabled": response.get("RotationEnabled", False),
                "rotation_lambda_arn": response.get("RotationLambdaARN"),
                "last_rotated_date": response.get("LastRotatedDate"),
                "last_changed_date": response.get("LastChangedDate"),
                "next_rotation_date": response.get("NextRotationDate"),
                "arn": response.get("ARN"),
            }

            if response.get("RotationEnabled"):
                summary["rotation_enabled"] += 1
                status_key = "enabled"
            else:
                summary["rotation_disabled"] += 1
                status_key = "disabled"

            summary["secrets"].append(secret_info)

            # Track by status
            if status_key not in summary["summary_by_status"]:
                summary["summary_by_status"][status_key] = []
            summary["summary_by_status"][status_key].append(secret_name)

        except ClientError as e:
            error_info = {
                "name": secret_name,
                "error": str(e),
                "error_code": e.response["Error"]["Code"]
                if hasattr(e, "response")
                else "Unknown",
            }
            summary["secrets"].append(error_info)

    # Calculate percentages
    if summary["total_secrets"] > 0:
        summary["rotation_enabled_percent"] = (
            summary["rotation_enabled"] / summary["total_secrets"]
        ) * 100
        summary["rotation_disabled_percent"] = (
            summary["rotation_disabled"] / summary["total_secrets"]
        ) * 100
    else:
        summary["rotation_enabled_percent"] = 0
        summary["rotation_disabled_percent"] = 0

    # Generate recommendations
    recommendations = []
    if summary["rotation_disabled"] > 0:
        recommendations.append(
            f"Enable rotation for {summary['rotation_disabled']} secret(s) without rotation"
        )

    # Check for stale rotations
    for secret in summary["secrets"]:
        if isinstance(secret, dict) and secret.get("rotation_enabled"):
            last_rotated = secret.get("last_rotated_date")
            if last_rotated:
                last_rotated_date = (
                    last_rotated.replace(tzinfo=None)
                    if hasattr(last_rotated, "tzinfo")
                    else last_rotated
                )
                days_since = (
                    (datetime.now() - last_rotated_date).days
                    if isinstance(last_rotated_date, datetime)
                    else None
                )
                if days_since and days_since > 90:
                    recommendations.append(
                        f"Secret '{secret['name']}' hasn't been rotated in {days_since} days"
                    )

    summary["recommendations"] = recommendations

    return summary
