import os
import requests
from identity_client import get_firebase_config
from identity_models import UserRegistrationRequest, UserRegistrationResponse


def register_user(
    email: str, password: str, display_name: str = None
) -> UserRegistrationResponse:
    """
    Creates a new email/password user account using Firebase Authentication.
    """
    config = get_firebase_config()
    api_key = config["api_key"]
    project_id = config["project_id"]

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}"

    payload = {"email": email, "password": password, "returnSecureToken": True}

    if display_name:
        payload["displayName"] = display_name

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    data = response.json()

    return UserRegistrationResponse(
        uid=data["localId"],
        email=data["email"],
        display_name=data.get("displayName", ""),
        id_token=data["idToken"],
        refresh_token=data["refreshToken"],
        expires_in=data["expiresIn"],
    )
