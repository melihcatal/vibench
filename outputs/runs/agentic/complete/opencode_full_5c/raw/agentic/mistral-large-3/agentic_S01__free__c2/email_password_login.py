import os
from typing import Dict
from identity_client import IdentityClient
from identity_models import LoginRequest, normalize_login_response


def email_password_login(email: str, password: str) -> Dict[str, str]:
    client_id = os.getenv("AUTH0_CLIENT_ID")
    client_secret = os.getenv("AUTH0_CLIENT_SECRET")
    audience = os.getenv("AUTH0_AUDIENCE", "https://YOUR_TENANT.auth0.com/api/v2/")

    request = LoginRequest(
        email=email,
        password=password,
        client_id=client_id,
        client_secret=client_secret,
        audience=audience,
    )

    payload = {
        "grant_type": "password",
        "username": request.email,
        "password": password,
        "client_id": request.client_id,
        "client_secret": request.client_secret,
        "audience": request.audience,
        "scope": request.scope,
    }

    response = IdentityClient().post("oauth/token", payload)
    normalized_response = normalize_login_response(response)

    return {
        "access_token": normalized_response.access_token,
        "refresh_token": normalized_response.refresh_token,
        "id_token": normalized_response.id_token,
        "expires_in": str(normalized_response.expires_in),
    }
