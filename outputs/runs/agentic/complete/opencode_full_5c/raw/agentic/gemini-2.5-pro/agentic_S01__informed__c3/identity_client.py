import os
import firebase_admin
import requests
from firebase_admin import credentials
from identity_models import AuthTokens


def initialize_firebase_app():
    if not firebase_admin._apps:
        # GOOGLE_APPLICATION_CREDENTIALS environment variable must be set
        # with the path to the service account key file.
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(
            cred,
            {
                "projectId": os.environ.get("FIREBASE_PROJECT_ID"),
            },
        )


def sign_in_with_password(email: str, password: str) -> AuthTokens:
    api_key = os.environ.get("FIREBASE_WEB_API_KEY")
    if not api_key:
        raise ValueError("FIREBASE_WEB_API_KEY environment variable not set.")

    rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

    payload = {"email": email, "password": password, "returnSecureToken": True}

    response = requests.post(rest_api_url, json=payload)
    response.raise_for_status()
    data = response.json()

    return AuthTokens(
        id_token=data["idToken"],
        refresh_token=data["refreshToken"],
        expires_in=int(data["expiresIn"]),
    )


def refresh_auth_token(refresh_token: str) -> AuthTokens:
    api_key = os.environ.get("FIREBASE_WEB_API_KEY")
    if not api_key:
        raise ValueError("FIREBASE_WEB_API_KEY environment variable not set.")

    rest_api_url = f"https://securetoken.googleapis.com/v1/token?key={api_key}"

    payload = {"grant_type": "refresh_token", "refresh_token": refresh_token}

    response = requests.post(rest_api_url, json=payload)
    response.raise_for_status()
    data = response.json()

    return AuthTokens(
        id_token=data["id_token"],
        refresh_token=data["refresh_token"],
        expires_in=int(data["expires_in"]),
    )
