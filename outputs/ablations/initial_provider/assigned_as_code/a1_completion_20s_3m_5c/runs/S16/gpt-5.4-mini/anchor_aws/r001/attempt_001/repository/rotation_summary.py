import boto3

from security_client import load_config


def rotation_summary(payload, config=None):
    config = load_config(config)
    client = boto3.client("secretsmanager", region_name=config.get("region"))
    response = client.describe_secret(SecretId=payload.get("secret_id") or payload.get("secret_name"))
    return {"rotation_enabled": response.get("RotationEnabled", False), "last_rotated_date": str(response.get("LastRotatedDate")) if response.get("LastRotatedDate") else None, "next_rotation_date": str(response.get("NextRotationDate")) if response.get("NextRotationDate") else None}
