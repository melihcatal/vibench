from __future__ import annotations

import os
from typing import Dict, Any

import boto3


def summarize_rotation(secret_id: str) -> Dict[str, Any]:
    client = boto3.client("secretsmanager", region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1")
    response = client.describe_secret(SecretId=secret_id)
    return {
        "secret_id": secret_id,
        "rotation_enabled": bool(response.get("RotationEnabled")),
        "last_rotated_date": str(response.get("LastRotatedDate")) if response.get("LastRotatedDate") else None,
        "next_rotation_date": str(response.get("NextRotationDate")) if response.get("NextRotationDate") else None,
        "rotation_lambda_arn": response.get("RotationLambdaARN"),
    }
