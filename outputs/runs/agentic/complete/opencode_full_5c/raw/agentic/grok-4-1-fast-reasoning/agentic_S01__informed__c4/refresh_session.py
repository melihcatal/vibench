import boto3
from botocore.exceptions import ClientError
from typing import Dict, Any
from identity_client import get_cognito_config
from identity_models import RefreshTokenRequest, RefreshTokenResponse


def refresh_session(request: RefreshTokenRequest) -> RefreshTokenResponse:
    config = get_cognito_config()
    client = boto3.client(
        "cognito-idp",
        aws_access_key_id=config["aws_access_key_id"],
        aws_secret_access_key=config["aws_secret_access_key"],
        region_name=config["region"],
    )
    try:
        resp = client.admin_initiate_auth(
            UserPoolId=config["user_pool_id"],
            ClientId=config["app_client_id"],
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={"REFRESH_TOKEN": request["refresh_token"]},
        )
        auth_result = resp["AuthenticationResult"]
        return {
            "access_token": auth_result["AccessToken"],
            "id_token": auth_result["IdToken"],
            "refresh_token": auth_result.get("RefreshToken", request["refresh_token"]),
            "expires_in": auth_result["ExpiresIn"],
        }
    except ClientError as e:
        raise ValueError(f"Refresh failed: {e}")
