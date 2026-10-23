import requests
from identity_client import Auth0Client
from identity_models import RegisterUserRequest, RegisterUserResponse


def register_user(request: RegisterUserRequest) -> RegisterUserResponse:
    client = Auth0Client()
    url = client.get_auth_url("/api/v2/users")
    headers = client.get_management_headers()
    payload = {
        "email": request.email,
        "password": request.password,
        "connection": request.connection,
        "email_verified": False,  # User will verify email later
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    user_data = response.json()
    return RegisterUserResponse(
        id=user_data["user_id"],
        email=user_data["email"],
        email_verified=user_data["email_verified"],
    )
