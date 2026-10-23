import requests
import os
from identity_client import FIREBASE_WEB_API_KEY
from identity_models import RegisterUserRequest, RegisterUserResponse

FIREBASE_SIGNUP_URL = "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key="

def register_user(request: RegisterUserRequest) -> RegisterUserResponse:
    if not FIREBASE_WEB_API_KEY:
        raise ValueError("Firebase Web API Key not found. Please set FIREBASE_API_KEY environment variable.")

    url = f"{FIREBASE_SIGNUP_URL}{FIREBASE_WEB_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "email": request.email,
        "password": request.password,
        "returnSecureToken": True
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status() # Raise an exception for HTTP errors

    data = response.json()
    return RegisterUserResponse(
        id_token=data["idToken"],
        refresh_token=data["refreshToken"],
        local_id=data["localId"]
    )
