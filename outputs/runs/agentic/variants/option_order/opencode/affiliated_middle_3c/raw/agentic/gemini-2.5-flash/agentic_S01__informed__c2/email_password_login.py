from identity_client import Auth0AuthenticationClient
from identity_models import LoginUserRequest, LoginUserResponse
import os


def email_password_login(request: LoginUserRequest) -> LoginUserResponse:
    client = Auth0AuthenticationClient()
    response = client.post(
        "oauth/token",
        {
            "client_id": client.client_id,
            "username": request.email,
            "password": request.password,
            "audience": request.audience,
            "scope": request.scope,
            "grant_type": request.grant_type,
        },
    )
    response.raise_for_status()
    data = response.json()
    return LoginUserResponse(
        access_token=data["access_token"],
        refresh_token=data.get("refresh_token"),
        id_token=data.get("id_token"),
        token_type=data["token_type"],
        expires_in=data["expires_in"],
    )
