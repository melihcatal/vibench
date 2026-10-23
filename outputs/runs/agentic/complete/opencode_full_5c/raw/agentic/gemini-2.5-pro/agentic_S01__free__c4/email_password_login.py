import os
import requests
from identity_models import UserCredentials, AuthResponse


def login_with_email_password(credentials: UserCredentials) -> AuthResponse:
    api_key = os.environ.get("FIREBASE_API_KEY")
    if not api_key:
        raise ValueError("FIREBASE_API_KEY environment variable not set.")

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

    payload = {
        "email": credentials.email,
        "password": credentials.password,
        "returnSecureToken": True,
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()

    return AuthResponse(
        id_token=data.get("idToken"),
        refresh_token=data.get("refreshToken"),
        expires_in=int(data.get("expiresIn")),
        local_id=data.get("localId"),
        is_new_user=data.get("isNewUser", False),
    )
