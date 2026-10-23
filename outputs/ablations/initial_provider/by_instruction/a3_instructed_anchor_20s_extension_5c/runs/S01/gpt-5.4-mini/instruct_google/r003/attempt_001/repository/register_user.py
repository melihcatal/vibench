import requests

from identity_client import GoogleIdentityClient
from identity_models import AccountCredentials


def register_user(email: str, password: str, display_name: str | None = None):
    client = GoogleIdentityClient()
    creds = AccountCredentials(email=email, password=password, display_name=display_name).normalized()
    response = client.session.post(
        "https://identitytoolkit.googleapis.com/v1/accounts:signUp",
        params={"key": client.key},
        json={
            "email": creds.email,
            "password": creds.password,
            "returnSecureToken": True,
            **({"displayName": creds.display_name} if creds.display_name else {}),
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
