import boto3
from datetime import datetime


def rotation_summary(payload, config=None):
    config = config or {}
    client = boto3.client("secretsmanager", region_name=config.get("region"))
    
    response = client.describe_secret(SecretId=payload["secret_id"])
    
    rotation_enabled = response.get("RotationEnabled", False)
    last_rotated_date = response.get("LastRotatedDate")
    next_rotation_date = response.get("NextRotationDate")
    rotation_status = response.get("RotationStatus")

    # Convert datetime objects to string for JSON serialization
    if last_rotated_date:  # Convert epoch to datetime string
        last_rotated_date = datetime.fromtimestamp(last_rotated_date.timestamp()).isoformat()
    if next_rotation_date:  # Convert epoch to datetime string
        next_rotation_date = datetime.fromtimestamp(next_rotation_date.timestamp()).isoformat()
    
    return {
        "secret_id": payload["secret_id"],
        "rotation_enabled": rotation_enabled,
        "last_rotated_date": last_rotated_date,
        "next_rotation_date": next_rotation_date,
        "rotation_status": rotation_status,
    }
