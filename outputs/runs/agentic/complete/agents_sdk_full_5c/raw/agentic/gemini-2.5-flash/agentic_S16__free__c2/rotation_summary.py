import os
import boto3
from datetime import datetime, timezone
from typing import List, Dict, Any

def summarize_secret_rotation_status(region_name: str = None) -> List[Dict[str, Any]]:
    """
    Summarizes the rotation status of secrets in AWS Secrets Manager.
    """
    if region_name is None:
        region_name = os.environ.get("AWS_REGION", "us-east-1")

    client = boto3.client("secretsmanager", region_name=region_name)

    summary = []
    paginator = client.get_paginator('list_secrets')
    pages = paginator.paginate(Filters=[{'Key': 'all', 'Values': ['true']}], IncludePlannedRotation=True)

    for page in pages:
        for secret in page['SecretList']:
            secret_summary = {
                "Name": secret.get("Name"),
                "Description": secret.get("Description"),
                "LastRotatedDate": secret.get("LastRotatedDate"),
                "NextRotationDate": secret.get("NextRotationDate"),
                "RotationEnabled": secret.get("RotationEnabled"),
                "RotationLambdaARN": secret.get("RotationLambdaARN"),
                "RotationRules": secret.get("RotationRules", {}).get("AutomaticallyAfterDays"),
                "Tags": secret.get("Tags", [])
            }
            summary.append(secret_summary)
    return summary

if __name__ == "__main__":
    # Example usage:
    # Set AWS_REGION and AWS credentials
    # rotation_status = summarize_secret_rotation_status()
    # for s in rotation_status:
    #     print(f"Secret: {s['Name']}\n  Rotation Enabled: {s['RotationEnabled']}\n  Last Rotated: {s['LastRotatedDate']}\n  Next Rotation: {s['NextRotationDate']}\n  Rotation Interval (days): {s['RotationRules']}\n")
    pass
