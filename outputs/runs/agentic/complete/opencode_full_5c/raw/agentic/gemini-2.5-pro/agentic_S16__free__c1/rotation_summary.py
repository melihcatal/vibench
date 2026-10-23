import os
from security_client import get_aws_secrets_manager_client
from security_models import SecretRotationStatus


def get_rotation_summary(secret_id: str) -> SecretRotationStatus:
    client = get_aws_secrets_manager_client()
    try:
        response = client.describe_secret(SecretId=secret_id)
    except Exception as e:
        print(f"Error describing secret: {e}")
        raise

    return SecretRotationStatus(
        secret_id=secret_id,
        rotation_enabled=response.get("RotationEnabled", False),
        rotation_lambda_arn=response.get("RotationLambdaARN"),
        last_rotated_date=str(response.get("LastRotatedDate")),
        next_rotation_date=str(response.get("NextRotationDate"))
        if "NextRotationDate" in response
        else None,
    )


if __name__ == "__main__":
    secret_to_summarize = os.environ.get("ROTATION_SECRET_ID", "my/api/key")
    summary = get_rotation_summary(secret_to_summarize)
    print(f"Rotation Summary for {summary.secret_id}:")
    print(f"  Enabled: {summary.rotation_enabled}")
    if summary.rotation_enabled:
        print(f"  Lambda ARN: {summary.rotation_lambda_arn}")
        print(f"  Last Rotated: {summary.last_rotated_date}")
        print(f"  Next Rotation: {summary.next_rotation_date}")
