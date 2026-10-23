import boto3


def summarize_rotation(secret_id: str):
    client = boto3.client("secretsmanager")
    metadata = client.describe_secret(SecretId=secret_id)
    return {
        "arn": metadata.get("ARN"),
        "rotation_enabled": metadata.get("RotationEnabled", False),
        "last_changed_date": metadata.get("LastChangedDate"),
        "last_rotated_date": metadata.get("LastRotatedDate"),
    }
