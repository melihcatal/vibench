import os

import boto3


def rotation_summary():
    client = boto3.client("secretsmanager", region_name=os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"))
    secret_id = os.environ["ROTATION_SUMMARY_SECRET_ID"]
    secret = client.describe_secret(SecretId=secret_id)
    return {
        "secret_id": secret_id,
        "rotation_enabled": secret.get("RotationEnabled", False),
        "last_rotated_date": secret.get("LastRotatedDate").isoformat() if secret.get("LastRotatedDate") else None,
        "rotation_rules": secret.get("RotationRules", {}),
    }
