import boto3
from security_models import SecretRequest


def rotation_summary(secret_id: str) -> dict:
    client = boto3.client("secretsmanager")
    request = SecretRequest(secret_id=secret_id)
    metadata = client.describe_secret(SecretId=request.secret_id)
    return {"secret_id": request.secret_id, "rotation_enabled": metadata.get("RotationEnabled", False), "last_rotated": metadata.get("LastRotatedDate")}
