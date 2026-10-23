from identity_client import Auth0ManagementClient
from identity_models import RegisterUserRequest, RegisterUserResponse


def register_user(request: RegisterUserRequest) -> RegisterUserResponse:
    client = Auth0ManagementClient()
    response = client.post(
        "api/v2/users",
        {
            "email": request.email,
            "password": request.password,
            "connection": request.connection,
        },
    )
    response.raise_for_status()
    data = response.json()
    return RegisterUserResponse(
        user_id=data["user_id"],
        email=data["email"],
        email_verified=data["email_verified"],
    )
