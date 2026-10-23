import os
import requests
from identity_client import FIREBASE_IDENTITY_TOOLKIT_URL, get_api_key
from identity_models import RegisterUserRequest, RegisterUserResponse

def register_user(request: RegisterUserRequest) -> RegisterUserResponse:
    api_key = get_api_key()
    url = f"{FIREBASE_IDENTITY_TOOLKIT_URL}signupNewUser?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "email": request["email"],
        "password": request["password"],
        "returnSecureToken": True
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()

    return {
        "idToken": data["idToken"],
        "refreshToken": data["refreshToken"],
        "expiresIn": data["expiresIn"],
        "email": data["email"],
        "localId": data["localId"]
    }