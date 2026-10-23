import requests
from identity_client import get_firebase_web_api_key
from identity_models import UserLoginRequest, AuthResponse


def email_password_login(login_request: UserLoginRequest) -> AuthResponse:
    api_key = get_firebase_web_api_key()
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

    payload = {
        "email": login_request.email,
        "password": login_request.password,
        "returnSecureToken": True,
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()  # Raise an exception for bad status codes

    return AuthResponse.model_validate(response.json())
