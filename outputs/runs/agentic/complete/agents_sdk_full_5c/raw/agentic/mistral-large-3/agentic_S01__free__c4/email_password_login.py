import os
from typing import Dict, Any
from identity_client import get_identity_client
from identity_models import LoginRequest, LoginResponse


def email_password_login(email: str, password: str) -> LoginResponse:
    client = get_identity_client()
    
    response = client.sign_in_with_email_and_password(
        email=email,
        password=password
    )
    
    return LoginResponse(
        access_token=response["access_token"],
        refresh_token=response["refresh_token"],
        expires_in=response["expires_in"]
    )