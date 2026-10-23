import os
from identity_client import get_cognito_client
from identity_models import UserRegistrationRequest, UserRegistrationResponse


def register_user(
    email: str, password: str, user_attributes: dict = None
) -> UserRegistrationResponse:
    """Create a new email/password user account using Amazon Cognito User Pools."""
    client = get_cognito_client()

    if user_attributes is None:
        user_attributes = {}

    user_attributes["email"] = email

    try:
        response = client.sign_up(
            ClientId=os.environ["COGNITO_CLIENT_ID"],
            Username=email,
            Password=password,
            UserAttributes=[{"Name": "email", "Value": email}],
        )

        user_sub = response["UserSub"]

        return UserRegistrationResponse(
            success=True,
            user_id=user_sub,
            email=email,
            message=f"User {email} registered successfully",
            requires_confirmation=response.get("UserConfirmed", False) is False,
        )
    except client.exceptions.UsernameExistsException:
        return UserRegistrationResponse(
            success=False,
            user_id=None,
            email=email,
            message=f"User with email {email} already exists",
            requires_confirmation=False,
        )
    except Exception as e:
        return UserRegistrationResponse(
            success=False,
            user_id=None,
            email=email,
            message=f"Registration failed: {str(e)}",
            requires_confirmation=False,
        )
