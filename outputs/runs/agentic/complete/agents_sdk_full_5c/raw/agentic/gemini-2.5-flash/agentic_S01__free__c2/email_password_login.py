import os
import requests
from identity_models import LoginUserRequest, LoginUserResponse

def email_password_login(request: LoginUserRequest) -> LoginUserResponse:
    firebase_api_key = os.environ.get("FIREBASE_API_KEY")
    if not firebase_api_key:
        raise ValueError("FIREBASE_API_KEY environment variable not set.")

    rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={firebase_api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "email": request.email,
        "password": request.password,
        "returnSecureToken": True
    }

    response = requests.post(rest_api_url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()

    return LoginUserResponse(
        id_token=data.get("idToken"),
        refresh_token=data.get("refreshToken"),
        expires_in=data.get("expiresIn"),
        local_id=data.get("localId")
    )
