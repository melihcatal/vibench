import requests
from identity_client import Auth0Client
from identity_models import LoginUserRequest, LoginUserResponse


def email_password_login(request: LoginUserRequest) -> LoginUserResponse:
    client = Auth0Client()
    url = client.get_auth_url("/oauth/token")
    headers = {"Content-Type": "application/json"}
    payload = {
        "grant_type": "password",
        "username": request.email,
        "password": request.password,
        "audience": request.audience,
        "scope": request.scope,
        "client_id": client.client_id,
        "client_secret": client.client_secret,
        "realm": request.realm,
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    token_data = response.json()
    return LoginUserResponse(
        access_token=token_data["access_token"],
        expires_in=token_data["expires_in"],
        id_token=token_data["id_token"],
        refresh_token=token_data.get("refresh_token", ""),
        token_type=token_data["token_type"],
    )
