import boto3
from botocore.exceptions import ClientError
from typing import Dict, Any
from identity_client import get_cognito_config
from identity_models import UserRegisterRequest, UserRegisterResponse


def register_user(request: UserRegisterRequest) -> UserRegisterResponse:
    config = get_cognito_config()
    client = boto3.client(
        "cognito-idp",
        aws_access_key_id=config["aws_access_key_id"],
        aws_secret_access_key=config["aws_secret_access_key"],
        region_name=config["region"],
    )
    email = request["email"]
    try:
        signup_resp = client.sign_up(
            ClientId=config["app_client_id"],
            Username=email,
            Password=request["password"],
            UserAttributes=[{"Name": "email", "Value": email}],
        )
        client.admin_confirm_sign_up(UserPoolId=config["user_pool_id"], Username=email)
        return {"user_sub": signup_resp["UserSub"]}
    except ClientError as e:
        raise ValueError(f"Registration failed: {e}")
