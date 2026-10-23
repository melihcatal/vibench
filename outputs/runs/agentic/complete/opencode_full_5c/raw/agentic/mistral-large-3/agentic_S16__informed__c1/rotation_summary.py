from typing import Dict, Optional
import os
import boto3
from datetime import datetime


def rotation_summary(secret_name: str) -> Optional[Dict]:
    """
    Summarizes secret rotation status from AWS Secrets Manager.
    """
    region_name = os.getenv("AWS_REGION", "us-east-1")

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        # Get secret metadata
        metadata = client.describe_secret(SecretId=secret_name)

        # Get current and previous versions
        versions = client.list_secret_version_ids(SecretId=secret_name)
        version_ids = [
            v["VersionId"] for v in versions["Versions"] if v["VersionStages"]
        ]

        current_version = next(
            (
                v["VersionId"]
                for v in versions["Versions"]
                if "AWSCURRENT" in v["VersionStages"]
            ),
            None,
        )

        previous_version = next(
            (
                v["VersionId"]
                for v in versions["Versions"]
                if "AWSPREVIOUS" in v["VersionStages"]
            ),
            None,
        )

        # Get rotation configuration
        rotation_enabled = metadata.get("RotationEnabled", False)
        rotation_lambda_arn = metadata.get("RotationLambdaARN", None)
        rotation_rules = metadata.get("RotationRules", {})
        automatically_after_days = rotation_rules.get("AutomaticallyAfterDays", 0)

        last_rotated = metadata.get("LastRotatedDate")
        next_rotation = metadata.get("NextRotationDate")

        return {
            "secret_name": secret_name,
            "current_version": current_version,
            "previous_version": previous_version,
            "rotation_enabled": rotation_enabled,
            "rotation_lambda_arn": rotation_lambda_arn,
            "automatically_after_days": automatically_after_days,
            "last_rotated": last_rotated.isoformat() if last_rotated else None,
            "next_rotation": next_rotation.isoformat() if next_rotation else None,
            "status": "healthy" if rotation_enabled else "disabled",
        }
    except Exception as e:
        print(f"Failed to summarize rotation status: {e}")
        return None
