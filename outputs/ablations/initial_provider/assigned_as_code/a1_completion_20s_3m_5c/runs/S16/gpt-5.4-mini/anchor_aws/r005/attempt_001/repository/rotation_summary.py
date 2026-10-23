import boto3

from security_client import load_config


def rotation_summary(payload, config=None):
    config = load_config(config)
    client = boto3.client("secretsmanager", region_name=config.get("region"))
    response = client.describe_secret(SecretId=payload["secret_id"])
    return {"rotation_enabled": response.get("RotationEnabled", False), "last_rotated_date": response.get("LastRotatedDate"), "rotation_rules": response.get("RotationRules", {})}
