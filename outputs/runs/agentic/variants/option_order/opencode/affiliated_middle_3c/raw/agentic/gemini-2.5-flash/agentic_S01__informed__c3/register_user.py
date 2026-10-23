import os
from identity_client import get_auth0_management_client
from identity_models import RegisterUserRequest, RegisterUserResponse


def register_user(request: RegisterUserRequest) -> RegisterUserResponse:
    management_client = get_auth0_management_client()
    user_data = {
        "email": request.email,
        "password": request.password,
        "connection": os.environ.get(
            "AUTH0_DB_CONNECTION", "Username-Password-Authentication"
        ),
    }
    new_user = management_client.users.create(user_data)
    return RegisterUserResponse(user_id=new_user["user_id"], email=new_user["email"])
