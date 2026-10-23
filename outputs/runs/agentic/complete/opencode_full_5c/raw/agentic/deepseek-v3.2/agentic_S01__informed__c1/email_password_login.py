import os
from identity_client import get_cognito_client
from identity_models import LoginRequest, LoginResponse


def email_password_login(email: str, password: str) -> LoginResponse:
    """Sign in a user with email and password and return tokens using Amazon Cognito."""
    client = get_cognito_client()

    try:
        response = client.initiate_auth(
            ClientId=os.environ["COGNITO_CLIENT_ID"],
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": email, "PASSWORD": password},
        )

        auth_result = response.get("AuthenticationResult", {})

        return LoginResponse(
            success=True,
            access_token=auth_result.get("AccessToken"),
            refresh_token=auth_result.get("RefreshToken"),
            id_token=auth_result.get("IdToken"),
            expires_in=auth_result.get("ExpiresIn"),
            token_type=auth_result.get("TokenType"),
            message="Login successful",
        )
    except client.exceptions.NotAuthorizedException:
        return LoginResponse(
            success=False,
            access_token=None,
            refresh_token=None,
            id_token=None,
            expires_in=None,
            token_type=None,
            message="Invalid email or password",
        )
    except client.exceptions.UserNotFoundException:
        return LoginResponse(
            success=False,
            access_token=None,
            refresh_token=None,
            id_token=None,
            expires_in=None,
            token_type=None,
            message="User not found",
        )
    except Exception as e:
        return LoginResponse(
            success=False,
            access_token=None,
            refresh_token=None,
            id_token=None,
            expires_in=None,
            token_type=None,
            message=f"Login failed: {str(e)}",
        )
