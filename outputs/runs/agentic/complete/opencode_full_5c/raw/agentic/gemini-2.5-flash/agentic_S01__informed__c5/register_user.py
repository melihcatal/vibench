import os
from identity_client import IdentityClient
from identity_models import RegisterUserRequest, RegisterUserResponse


def register_user(request: RegisterUserRequest) -> RegisterUserResponse:
    identity_client = IdentityClient()
    user = identity_client.management_client.users.create(
        {
            "email": request.email,
            "password": request.password,
            "connection": request.connection,
            "given_name": request.given_name,
            "family_name": request.family_name,
        }
    )
    return RegisterUserResponse(
        id=user["user_id"], email=user["email"], email_verified=user["email_verified"]
    )
