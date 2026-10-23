import os
import boto3
from typing import List
from security_models import SecretRotationSummary

def get_aws_secret_rotation_summary(region_name: str = None) -> List[SecretRotationSummary]:
    """
    Summarizes secret rotation status from AWS Secrets Manager.
    """
    if region_name is None:
        region_name = os.environ.get("AWS_REGION", "us-east-1")
    client = boto3.client("secretsmanager", region_name=region_name)

    summaries: List[SecretRotationSummary] = []
    paginator = client.get_paginator('list_secrets')

    for page in paginator.paginate():
        for secret in page.get('SecretList', []):
            secret_arn = secret.get('ARN')
            secret_name = secret.get('Name')
            rotation_enabled = secret.get('RotationEnabled', False)
            last_rotated_date = secret.get('LastRotatedDate')
            next_rotation_date = secret.get('NextRotationDate')

            status = "UNKNOWN"
            if rotation_enabled:
                if last_rotated_date:
                    status = "ROTATED"
                else:
                    status = "ROTATION_ENABLED_NEVER_ROTATED"
            else:
                status = "ROTATION_DISABLED"

            summaries.append(SecretRotationSummary(
                secret_id=secret_arn,
                status=status,
                last_rotated_at=str(last_rotated_date) if last_rotated_date else None,
                next_rotation_at=str(next_rotation_date) if next_rotation_date else None,
                notes=f"Rotation {'enabled' if rotation_enabled else 'disabled'}."
            ))
    return summaries
