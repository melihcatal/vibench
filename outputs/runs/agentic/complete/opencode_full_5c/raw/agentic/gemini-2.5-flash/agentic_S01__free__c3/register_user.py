import os
import boto3
from identity_models import UserRegistrationRequest, UserRegistrationResponse
from identity_client import (
    get_cognito_client,
    get_cognito_user_pool_id,
    get_cognito_client_id,
)


def register_user(request: UserRegistrationRequest) -> UserRegistrationResponse:
    cognito_client = get_cognito_client()
    user_pool_id = request.user_pool_id
    client_id = request.client_id

    try:
        response = cognito_client.sign_up(
            ClientId=client_id,
            Username=request.email,  # Cognito often uses email as username
            Password=request.password,
            UserAttributes=[
                {"Name": "email", "Value": request.email},
            ],
        )
        return UserRegistrationResponse(
            user_confirmed=response["UserConfirmed"], user_sub=response["UserSub"]
        )
    except cognito_client.exceptions.UsernameExistsException:
        # Handle user already exists error
        raise ValueError("User with this email already exists.")
    except Exception as e:
        # General error handling
        raise RuntimeError(f"Cognito registration failed: {e}")


if __name__ == "__main__":
    # Example usage (requires environment variables to be set)
    os.environ["AWS_REGION"] = "us-east-1"
    os.environ["COGNITO_USER_POOL_ID"] = "YOUR_USER_POOL_ID"
    os.environ["COGNITO_CLIENT_ID"] = "YOUR_CLIENT_ID"

    try:
        reg_request = UserRegistrationRequest(
            email="testuser@example.com",
            password="StrongPassword123!",
            client_id=get_cognito_client_id(),
            user_pool_id=get_cognito_user_pool_id(),
        )
        response = register_user(reg_request)
        print(
            f"User registration successful: {response.user_confirmed}, User Sub: {response.user_sub}"
        )
    except Exception as e:
        print(f"Error during registration: {e}")
