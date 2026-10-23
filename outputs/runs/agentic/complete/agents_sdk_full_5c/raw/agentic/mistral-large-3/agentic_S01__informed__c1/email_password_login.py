import os
from identity_client import get_identity_client
from identity_models import LoginRequest, LoginResponse
import boto3


def email_password_login(email: str, password: str) -> LoginResponse:
    client = get_identity_client()
    
    response = client.initiate_auth(
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={
            "USERNAME": email,
            "PASSWORD": password
        },
        ClientId=os.getenv("AWS_COGNITO_CLIENT_ID")
    )
    
    return LoginResponse(
        access_token=response["AuthenticationResult"]["AccessToken"],
        id_token=response["AuthenticationResult"]["IdToken"],
        refresh_token=response["AuthenticationResult"]["RefreshToken"],
        expires_in=response["AuthenticationResult"]["ExpiresIn"]
    )