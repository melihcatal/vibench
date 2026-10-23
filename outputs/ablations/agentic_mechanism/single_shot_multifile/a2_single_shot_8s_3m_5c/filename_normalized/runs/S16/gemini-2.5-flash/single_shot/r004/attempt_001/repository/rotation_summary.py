import os
import boto3
from typing import List
from security_models import SecretMetadata

def summarize_secret_rotation_status() -> List[SecretMetadata]:
    aws_region = os.getenv('AWS_REGION', 'us-east-1')
    client = boto3.client('secretsmanager', region_name=aws_region)

    secrets_summary: List[SecretMetadata] = []
    paginator = client.get_paginator('list_secrets')

    try:
        for page in paginator.paginate():
            for secret in page.get('SecretList', []):
                secrets_summary.append(
                    SecretMetadata(
                        name=secret.get('Name'),
                        arn=secret.get('ARN'),
                        description=secret.get('Description'),
                        last_rotated_date=secret.get('LastRotatedDate').isoformat() if secret.get('LastRotatedDate') else None,
                        rotation_enabled=secret.get('RotationEnabled', False),
                        tags={tag['Key']: tag['Value'] for tag in secret.get('Tags', [])}
                    )
                )
        return secrets_summary
    except Exception as e:
        raise RuntimeError(f"Error summarizing secret rotation status from AWS Secrets Manager: {e}")
