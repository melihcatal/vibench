import boto3
from botocore.exceptions import ClientError
from typing import Dict, Any
from identity_client import get_cognito_config
from identity_models import PasswordResetRequest, PasswordResetResponse


def password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    config = get_cognito_config()
    client = boto3.client(
        "cognito-idp",
        aws_access_key_id=config["aws_access_key_id"],
        aws_secret_access_key=config["aws_secret_access_key"],
        region_name=config["region"],
    )
    try:
        client.forgot_password(
            ClientId=config["app_client_id"], Username=request["email"]
        )
        return {"status": "reset_initiated"}
    except ClientError as e:
        raise ValueError(f"Password reset initiation failed: {e}")
