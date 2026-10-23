import os
import boto3
from identity_models import UserLoginRequest, UserLoginResponse
from identity_client import (
    get_cognito_client,
    get_cognito_user_pool_id,
    get_cognito_client_id,
)


def email_password_login(request: UserLoginRequest) -> UserLoginResponse:
    cognito_client = get_cognito_client()
    user_pool_id = request.user_pool_id
    client_id = request.client_id

    try:
        response = cognito_client.initiate_auth(
            ClientId=client_id,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": request.email, "PASSWORD": request.password},
        )

        auth_result = response["AuthenticationResult"]
        return UserLoginResponse(
            access_token=auth_result["AccessToken"],
            id_token=auth_result["IdToken"],
            refresh_token=auth_result["RefreshToken"],
            expires_in=auth_result["ExpiresIn"],
        )
    except cognito_client.exceptions.NotAuthorizedException:
        raise ValueError("Incorrect username or password.")
    except cognito_client.exceptions.UserNotFoundException:
        raise ValueError("User not found.")
    except Exception as e:
        raise RuntimeError(f"Cognito login failed: {e}")


if __name__ == "__main__":
    # Example usage (requires environment variables to be set)
    os.environ["AWS_REGION"] = "us-east-1"
    os.environ["COGNITO_USER_POOL_ID"] = "YOUR_USER_POOL_ID"
    os.environ["COGNITO_CLIENT_ID"] = "YOUR_CLIENT_ID"

    try:
        login_request = UserLoginRequest(
            email="testuser@example.com",
            password="StrongPassword123!",
            client_id=get_cognito_client_id(),
            user_pool_id=get_cognito_user_pool_id(),
        )
        response = email_password_login(login_request)
        print(
            f"Login successful. Access Token: {response.access_token[:10]}..., Expires in: {response.expires_in}s"
        )
    except Exception as e:
        print(f"Error during login: {e}")
