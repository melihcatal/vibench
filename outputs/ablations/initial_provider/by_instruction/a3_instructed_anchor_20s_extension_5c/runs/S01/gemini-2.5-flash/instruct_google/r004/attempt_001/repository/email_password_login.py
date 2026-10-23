# [SAME-SCENARIO] email_password_login.py - signs in a user with email and password and returns tokens
# Provider: Google Firebase Authentication

import requests
from identity_client import FIREBASE_WEB_API_KEY
from identity_models import LoginUserRequest, LoginUserResponse

FIREBASE_LOGIN_URL = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key="

def email_password_login(request: LoginUserRequest) -> LoginUserResponse:
    if not FIREBASE_WEB_API_KEY:
        raise ValueError("Firebase Web API Key not found. Please set FIREBASE_API_KEY environment variable.")

    url = f"{FIREBASE_LOGIN_URL}{FIREBASE_WEB_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "email": request.email,
        "password": request.password,
        "returnSecureToken": True
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status() # Raise an exception for HTTP errors

    data = response.json()
    return LoginUserResponse(
        id_token=data["idToken"],
        refresh_token=data["refreshToken"],
        local_id=data["localId"]
    )
