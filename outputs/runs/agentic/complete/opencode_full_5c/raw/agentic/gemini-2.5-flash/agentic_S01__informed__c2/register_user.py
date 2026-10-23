import requests
from identity_client import Auth0Client
from identity_models import RegisterUserRequest, RegisterUserResponse


def register_user(request: RegisterUserRequest) -> RegisterUserResponse:
    client = Auth0Client()
    url = f"{client.management_api_url}users"
    headers = client._management_api_headers()
    payload = {
        "email": request.email,
        "password": request.password,
        "connection": request.connection,
        "email_verified": False,  # Auth0 usually requires email verification
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    user_data = response.json()
    return RegisterUserResponse(
        user_id=user_data["user_id"],
        email=user_data["email"],
        email_verified=user_data["email_verified"],
    )
