import os
from identity_client import get_identity_client
from identity_models import RegisterRequest, RegisterResponse

def register_user(email: str, password: str, display_name: str) -> RegisterResponse:
    client = get_identity_client()
    request = RegisterRequest(
        email=email,
        password=password,
        display_name=display_name
    )
    response = client.create_user(
        email=request.email,
        password=request.password,
        display_name=request.display_name
    )
    return RegisterResponse(
        user_id=response["user"]["id"],
        email=response["user"]["email"],
        display_name=response["user"]["displayName"]
    )