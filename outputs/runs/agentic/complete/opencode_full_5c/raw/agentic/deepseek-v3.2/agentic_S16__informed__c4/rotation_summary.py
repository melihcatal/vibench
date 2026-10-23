import os
import boto3
from datetime import datetime, timezone
from typing import Dict, List, Any


def rotation_summary(
    secret_names: List[str], region_name: str = None
) -> Dict[str, Any]:
    """Summarize secret rotation status using AWS Secrets Manager."""
    if region_name is None:
        region_name = os.environ.get("AWS_REGION", "us-east-1")

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    summary = {
        "total_secrets": len(secret_names),
        "rotation_enabled": 0,
        "rotation_disabled": 0,
        "secrets": [],
    }

    for secret_name in secret_names:
        try:
            response = client.describe_secret(SecretId=secret_name)

            rotation_enabled = response.get("RotationEnabled", False)
            last_rotated = response.get("LastRotatedDate")
            last_changed = response.get("LastChangedDate")
            next_rotation = response.get("NextRotationDate")

            if rotation_enabled:
                summary["rotation_enabled"] += 1
            else:
                summary["rotation_disabled"] += 1

            secret_info = {
                "secret_name": secret_name,
                "rotation_enabled": rotation_enabled,
                "last_changed": last_changed.isoformat() if last_changed else None,
                "last_rotated": last_rotated.isoformat() if last_rotated else None,
                "next_rotation": next_rotation.isoformat() if next_rotation else None,
                "rotation_lambda_arn": response.get("RotationLambdaARN"),
                "rotation_rules": response.get("RotationRules"),
                "arn": response.get("ARN"),
            }

            summary["secrets"].append(secret_info)

        except Exception as e:
            error_info = {
                "secret_name": secret_name,
                "error": str(e),
                "rotation_enabled": False,
                "last_changed": None,
                "last_rotated": None,
                "next_rotation": None,
            }
            summary["secrets"].append(error_info)
            summary["rotation_disabled"] += 1

    summary["rotation_percentage"] = (
        (summary["rotation_enabled"] / summary["total_secrets"] * 100)
        if summary["total_secrets"] > 0
        else 0
    )

    return summary
