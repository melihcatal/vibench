import os
import requests
from identity_models import UserLoginPayload, AuthTokens
from identity_client import get_firebase_app


def email_password_login(payload: UserLoginPayload) -> AuthTokens:
    # Initialize Firebase app if not already done, to ensure project_id is available
    app = get_firebase_app()
    project_id = app.project_id

    api_key = os.getenv("FIREBASE_WEB_API_KEY")
    if not api_key:
        raise ValueError("FIREBASE_WEB_API_KEY environment variable not set.")

    # Firebase Authentication REST API endpoint for email/password sign-in
    rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

    headers = {"Content-Type": "application/json"}
    data = {
        "email": payload.email,
        "password": payload.password,
        "returnSecureToken": True
    }

    response = requests.post(rest_api_url, json=data, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors

    response_data = response.json()

    return AuthTokens(
        id_token=response_data["idToken"],
        refresh_token=response_data["refreshToken"],
        expires_in=int(response_data["expiresIn"]),
        local_id=response_data["localId"]
    )
