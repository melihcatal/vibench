from __future__ import annotations

from identity_client import auth0_client_id, auth0_connection, get_client
from identity_models import TokenSet, UserCredentials


def login_with_email_password(email: str, password: str) -> TokenSet:
    creds = UserCredentials.from_mapping({"email": email, "password": password})
    client = get_client()
    response = client.session.post(
        f"{client.oauth_base}/oauth/token",
        json={
            "grant_type": "http://auth0.com/oauth/grant-type/password-realm",
            "client_id": auth0_client_id(),
            "username": creds.email,
            "password": creds.password,
            "realm": auth0_connection(),
            "scope": "openid profile email offline_access",
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return TokenSet(
        access_token=data["access_token"],
        refresh_token=data.get("refresh_token"),
        id_token=data.get("id_token"),
        expires_in=data.get("expires_in"),
    )
