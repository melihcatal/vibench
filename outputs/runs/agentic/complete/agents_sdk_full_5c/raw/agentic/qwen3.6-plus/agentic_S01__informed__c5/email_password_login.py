"""
email_password_login.py
Signs in a user with email and password and returns tokens via Amazon Cognito User Pools.

Provider: Amazon Cognito User Pools (boto3 SDK)
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

import os
import boto3
from botocore.exceptions import ClientError
from identity_client import get_cognito_client, COGNITO_CLIENT_ID
from identity_models import LoginRequest, LoginResponse


def login_user(request: LoginRequest) -> LoginResponse:
    """
    Authenticates a user with email/password against Amazon Cognito User Pools.

    Args:
        request: LoginRequest containing email and password.

    Returns:
        LoginResponse with access token, id token, refresh token, and expiry.
    """
    cognito_idp = get_cognito_client()

    try:
        response = cognito_idp.initiate_auth(
            ClientId=COGNITO_CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": request.email,
                "PASSWORD": request.password,
            },
        )

        auth_result = response.get("AuthenticationResult", {})

        return LoginResponse(
            access_token=auth_result.get("AccessToken"),
            id_token=auth_result.get("IdToken"),
            refresh_token=auth_result.get("RefreshToken"),
            token_type=auth_result.get("TokenType", "Bearer"),
            expires_in=auth_result.get("ExpiresIn", 3600),
        )
    except ClientError as exc:
        error_code = exc.response["Error"]["Code"]
        raise RuntimeError(f"Cognito login failed: {error_code} - {exc.response['Error']['Message']}")


if __name__ == "__main__":
    req = LoginRequest(email="user@example.com", password="SecureP@ssw0rd!")
    resp = login_user(req)
    print(f"Logged in. Token expires in {resp.expires_in}s")
