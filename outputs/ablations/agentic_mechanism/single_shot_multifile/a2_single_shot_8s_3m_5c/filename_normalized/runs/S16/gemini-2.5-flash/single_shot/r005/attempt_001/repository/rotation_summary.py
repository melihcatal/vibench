import os
from security_client import get_secrets_manager_client

def summarize_secret_rotation_status() -> list[dict]:
    client = get_secrets_manager_client()
    rotation_summary = []
    paginator = client.get_paginator('list_secrets')

    try:
        for page in paginator.paginate():
            for secret in page.get('SecretList', []):
                secret_arn = secret['ARN']
                secret_name = secret['Name']
                
                describe_response = client.describe_secret(SecretId=secret_arn)
                
                rotation_enabled = describe_response.get('RotationEnabled', False)
                last_rotated_date = describe_response.get('LastRotatedDate')

                summary_item = {
                    "SecretName": secret_name,
                    "RotationEnabled": rotation_enabled,
                    "LastRotatedDate": last_rotated_date.isoformat() if last_rotated_date else None,
                    "RotationLambdaARN": describe_response.get('RotationLambdaARN'),
                    "RotationRules": describe_response.get('RotationRules')
                }
                rotation_summary.append(summary_item)
    except Exception:
        raise
    
    return rotation_summary
