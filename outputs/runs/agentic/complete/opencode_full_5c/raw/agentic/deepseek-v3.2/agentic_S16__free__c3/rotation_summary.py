import os
import boto3
from datetime import datetime, timedelta
from typing import List, Dict, Any
from botocore.exceptions import ClientError


def rotation_summary(secret_names: List[str] = None) -> Dict[str, Any]:
    """
    Summarize secret rotation status for AWS Secrets Manager secrets.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        if secret_names is None:
            response = client.list_secrets(MaxResults=100)
            secret_names = [secret["Name"] for secret in response.get("SecretList", [])]

        summary = {
            "provider": "aws",
            "region": region_name,
            "timestamp": datetime.utcnow().isoformat(),
            "secrets": [],
            "rotation_stats": {
                "total_secrets": 0,
                "with_rotation_enabled": 0,
                "with_pending_versions": 0,
                "stale_secrets": 0,
            },
        }

        for secret_name in secret_names:
            try:
                secret_detail = client.describe_secret(SecretId=secret_name)

                rotation_enabled = secret_detail.get("RotationEnabled", False)
                rotation_rules = secret_detail.get("RotationRules", {})
                last_rotated_date = secret_detail.get("LastRotatedDate")
                last_changed_date = secret_detail.get("LastChangedDate")

                versions = {}
                try:
                    version_response = client.list_secret_version_ids(
                        SecretId=secret_name
                    )
                    for version in version_response.get("Versions", []):
                        version_id = version.get("VersionId")
                        version_stages = version.get("VersionStages", [])

                        if "AWSCURRENT" in version_stages:
                            versions["current"] = version_id
                        if "AWSPENDING" in version_stages:
                            versions["pending"] = version_id
                        if "AWSPREVIOUS" in version_stages:
                            versions["previous"] = version_id
                except ClientError:
                    pass

                is_stale = False
                if last_changed_date:
                    days_since_change = (
                        datetime.utcnow() - last_changed_date.replace(tzinfo=None)
                    ).days
                    is_stale = days_since_change > 90

                secret_info = {
                    "name": secret_name,
                    "rotation_enabled": rotation_enabled,
                    "rotation_lambda_arn": secret_detail.get("RotationLambdaARN"),
                    "last_rotated": last_rotated_date.isoformat()
                    if last_rotated_date
                    else None,
                    "last_changed": last_changed_date.isoformat()
                    if last_changed_date
                    else None,
                    "versions": versions,
                    "is_stale": is_stale,
                    "days_since_change": days_since_change
                    if last_changed_date
                    else None,
                    "arn": secret_detail.get("ARN"),
                }

                summary["secrets"].append(secret_info)
                summary["rotation_stats"]["total_secrets"] += 1

                if rotation_enabled:
                    summary["rotation_stats"]["with_rotation_enabled"] += 1
                if "pending" in versions:
                    summary["rotation_stats"]["with_pending_versions"] += 1
                if is_stale:
                    summary["rotation_stats"]["stale_secrets"] += 1

            except ClientError as e:
                error_secret = {"name": secret_name, "error": str(e), "arn": None}
                summary["secrets"].append(error_secret)

        summary["rotation_stats"]["rotation_percentage"] = (
            (
                summary["rotation_stats"]["with_rotation_enabled"]
                / summary["rotation_stats"]["total_secrets"]
                * 100
            )
            if summary["rotation_stats"]["total_secrets"] > 0
            else 0
        )

        return summary

    except ClientError as e:
        raise RuntimeError(f"Error generating rotation summary: {e}") from e
