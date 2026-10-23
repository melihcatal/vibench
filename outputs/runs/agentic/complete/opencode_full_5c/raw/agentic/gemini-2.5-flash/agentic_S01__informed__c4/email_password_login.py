import requests
from identity_client import auth0_client
from identity_models import UserLoginRequest, AuthResponse


def email_password_login(request: UserLoginRequest) -> AuthResponse:
    """Signs in a user with email and password and returns tokens using Auth0 Authentication API."""
    payload = {
        "grant_type": "password",
        "username": request.email,
        "password": request.password,
        "scope": request.scope,
        "client_id": auth0_client.client_id,
        "client_secret": auth0_client.client_secret,
        "realm": request.realm,
    }
    if request.audience:
        payload["audience"] = request.audience

    try:
        response = requests.post(auth0_client.authentication_url, json=payload)
        response.raise_for_status()
        data = response.json()

        return AuthResponse(
            access_token=data["access_token"],
            expires_in=data["expires_in"],
            token_type=data["token_type"],
            refresh_token=data.get("refresh_token"),
            id_token=data.get("id_token"),
        )
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Auth0 email/password login failed: {e}")
