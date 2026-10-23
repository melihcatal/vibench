import os
import sys
import boto3

# Extend the system path to include the current directory for local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from identity_client import IdentityClient
from identity_models import RegisterUserRequest, RegisterUserResponse


def register_user(request: RegisterUserRequest) -> RegisterUserResponse:
    identity_client = IdentityClient()
    cognito_client = identity_client.get_cognito_idp_client()
    client_id = identity_client.get_client_id()

    try:
        response = cognito_client.sign_up(
            ClientId=client_id,
            Username=request.email,
            Password=request.password,
            UserAttributes=[
                {"Name": "email", "Value": request.email},
            ],
        )
        user_id = response[
            "UserConfirmed"
        ]  # This indicates if the user is confirmed immediately or needs verification
        # In a real scenario, you'd likely want to return response['UserSub'] after confirmation
        # For this example, we'll return a generic user_id and a confirmation message.
        return RegisterUserResponse(
            user_id=request.email,
            message="User registration initiated. Please confirm your email.",
        )
    except cognito_client.exceptions.UsernameExistsException:
        return RegisterUserResponse(
            user_id=request.email, message="User with this email already exists."
        )
    except Exception as e:
        return RegisterUserResponse(
            user_id="", message=f"Registration failed: {str(e)}"
        )
