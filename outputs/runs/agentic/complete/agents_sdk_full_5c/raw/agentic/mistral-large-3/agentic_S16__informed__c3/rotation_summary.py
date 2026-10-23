import os
import boto3
from typing import Dict, List

def summarize_rotation_status(secret_names: List[str]) -> Dict[str, str]:
    """
    Summarize secret rotation status using AWS Secrets Manager.
    """
    client = boto3.client(
        "secretsmanager",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    )
    
    summary = {}
    for secret_name in secret_names:
        response = client.describe_secret(SecretId=secret_name)
        last_rotated = response.get("LastRotatedDate", "Never")
        summary[secret_name] = str(last_rotated)
    
    return summary