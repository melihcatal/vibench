import requests
import os
from identity_models import EmailPasswordLoginRequest, EmailPasswordLoginResponse

def email_password_login(payload: EmailPasswordLoginRequest):
    api_key = os.environ.get("FIREBASE_WEB_API_KEY")
    if not api_key:
        raise ValueError("FIREBASE_WEB_API_KEY environment variable not set.")

    rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "email": payload.email,
        "password": payload.password,
        "returnSecureToken": True
    }

    response = requests.post(rest_api_url, headers=headers, json=data)
    response.raise_for_status()
    response_data = response.json()

    return EmailPasswordLoginResponse(
        id_token=response_data["idToken"],
        refresh_token=response_data["refreshToken"],
        expires_in=response_data["expiresIn"]
    )
