import os
from identity_client import get_auth0_management_client
from identity_models import RegisterUserRequest, RegisterUserResponse

def register_user(email: str, password: str, username: str = None) -> RegisterUserResponse:
    client = get_auth0_management_client()
    
    user_data = {
        "email": email,
        "password": password,
        "connection": "Username-Password-Authentication",
        "email_verified": False,
    }
    if username:
        user_data["username"] = username
    
    user = client.users.create(body=user_data)
    return RegisterUserResponse(
        user_id=user["user_id"],
        email=user["email"],
        created_at=user["created_at"]
    )