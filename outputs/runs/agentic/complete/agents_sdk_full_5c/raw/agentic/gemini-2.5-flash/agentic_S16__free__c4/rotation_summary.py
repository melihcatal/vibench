import boto3
import os
from typing import List, Dict, Any
from datetime import datetime

def summarize_secret_rotation_status() -> List[Dict[str, Any]]:
    """
    Summarizes the rotation status of secrets managed by AWS Secrets Manager.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    client = boto3.client("secretsmanager", region_name=region_name)

    summaries = []
    paginator = client.get_paginator('list_secrets')
    response_iterator = paginator.paginate()

    for page in response_iterator:
        for secret in page.get('SecretList', []):
            secret_name = secret.get('Name')
            rotation_enabled = secret.get('RotationEnabled', False)
            last_rotated_date_ts = secret.get('LastRotatedDate')
            
            # Rotation rules are often part of the rotation lambda configuration,
            # not directly in list_secrets output. We'll indicate if rotation is enabled.
            
            summary = {
                "secret_name": secret_name,
                "arn": secret.get('ARN'),
                "description": secret.get('Description'),
                "rotation_enabled": rotation_enabled,
                "last_rotated_date": datetime.fromtimestamp(last_rotated_date_ts).isoformat() if last_rotated_date_ts else None,
            }
            summaries.append(summary)
            
    return summaries

