import os

from security_client import get_secrets_client


def rotation_summary(secret_id: str = None):
    client = get_secrets_client()
    secret_id = secret_id or os.getenv("AWS_SECRET_ROTATE_ID", "rotation/secret")
    response = client.describe_secret(SecretId=secret_id)
    return {
        "secret_id": secret_id,
        "rotation_enabled": response.get("RotationEnabled"),
        "rotation_lambda_arn": response.get("RotationLambdaARN"),
        "last_rotated_date": response.get("LastRotatedDate"),
    }
