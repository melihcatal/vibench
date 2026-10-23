import boto3


def rotation_summary(secret_id: str) -> dict:
    client = boto3.client("secretsmanager")
    response = client.describe_secret(SecretId=secret_id)
    return {
        "SecretId": secret_id,
        "RotationEnabled": response.get("RotationEnabled", False),
        "LastRotatedDate": response.get("LastRotatedDate").isoformat()
        if response.get("LastRotatedDate")
        else None,
    }
