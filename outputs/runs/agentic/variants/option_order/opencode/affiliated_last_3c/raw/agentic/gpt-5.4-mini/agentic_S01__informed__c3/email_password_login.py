import os

import requests

from identity_client import auth0_domain
from identity_models import TokenSet, UserCredentials


def email_password_login(email: str, password: str) -> TokenSet:
    credentials = UserCredentials(email=email, password=password).normalized()
    resp = requests.post(
        f"https://{auth0_domain()}/oauth/token",
        json={
            "grant_type": "password",
            "username": credentials.email,
            "password": credentials.password,
            "audience": os.environ.get("AUTH0_AUDIENCE", ""),
            "client_id": os.environ.get("AUTH0_CLIENT_ID", ""),
            "client_secret": os.environ.get("AUTH0_CLIENT_SECRET", ""),
            "scope": "openid profile email offline_access",
        },
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    return TokenSet(
        access_token=data["access_token"],
        refresh_token=data.get("refresh_token"),
        id_token=data.get("id_token"),
        expires_in=data.get("expires_in"),
    )
