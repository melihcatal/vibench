import boto3


def rotation_summary(secret_id: str, region_name: str | None = None) -> dict:
    client = boto3.client("secretsmanager", region_name=region_name)
    response = client.describe_secret(SecretId=secret_id)
    return {
        "secret_id": secret_id,
        "rotation_enabled": response.get("RotationEnabled", False),
        "last_rotated_date": response.get("LastRotatedDate"),
    }
