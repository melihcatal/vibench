import os
import requests
from identity_models import RegisterUserRequest, RegisterUserResponse

def register_user(request: RegisterUserRequest) -> RegisterUserResponse:
    firebase_api_key = os.environ.get("FIREBASE_API_KEY")
    if not firebase_api_key:
        raise ValueError("FIREBASE_API_KEY environment variable not set.")

    rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={firebase_api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "email": request.email,
        "password": request.password,
        "returnSecureToken": True
    }

    response = requests.post(rest_api_url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()

    return RegisterUserResponse(
        id_token=data.get("idToken"),
        refresh_token=data.get("refreshToken"),
        expires_in=data.get("expiresIn"),
        local_id=data.get("localId")
    )
