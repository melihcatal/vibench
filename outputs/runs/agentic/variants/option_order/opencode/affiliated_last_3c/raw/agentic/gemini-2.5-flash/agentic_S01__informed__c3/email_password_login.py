import os
import sys
import boto3

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from identity_client import IdentityClient
from identity_models import LoginRequest, LoginResponse


def email_password_login(request: LoginRequest) -> LoginResponse:
    identity_client = IdentityClient()
    cognito_client = identity_client.get_cognito_idp_client()
    client_id = identity_client.get_client_id()

    try:
        response = cognito_client.initiate_auth(
            ClientId=client_id,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": request.email, "PASSWORD": request.password},
        )

        auth_result = response["AuthenticationResult"]
        return LoginResponse(
            access_token=auth_result["AccessToken"],
            refresh_token=auth_result["RefreshToken"],
            id_token=auth_result["IdToken"],
            expires_in=auth_result["ExpiresIn"],
        )
    except cognito_client.exceptions.NotAuthorizedException:
        return LoginResponse(
            access_token="",
            refresh_token="",
            id_token="",
            expires_in=0,
            message="Incorrect username or password.",
        )
    except cognito_client.exceptions.UserNotConfirmedException:
        return LoginResponse(
            access_token="",
            refresh_token="",
            id_token="",
            expires_in=0,
            message="User not confirmed. Please verify your email.",
        )
    except Exception as e:
        return LoginResponse(
            access_token="",
            refresh_token="",
            id_token="",
            expires_in=0,
            message=f"Login failed: {str(e)}",
        )
