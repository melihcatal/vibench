from __future__ import annotations

from typing import Any, Dict

import boto3

AWS_REGION = "us-east-1"


def rotation_summary(secret_id: str) -> Dict[str, Any]:
    client = boto3.client("secretsmanager", region_name=AWS_REGION)
    response = client.describe_secret(SecretId=secret_id)
    rotation_enabled = bool(response.get("RotationEnabled"))
    return {
        "provider": "AWS Secrets Manager",
        "secret_id": secret_id,
        "rotation_enabled": rotation_enabled,
        "rotation_lambda_arn": response.get("RotationLambdaARN"),
        "last_rotated_date": response.get("LastRotatedDate"),
        "next_rotation_date": response.get("NextRotationDate"),
        "version_ids_to_stages": response.get("VersionIdsToStages", {}),
    }
