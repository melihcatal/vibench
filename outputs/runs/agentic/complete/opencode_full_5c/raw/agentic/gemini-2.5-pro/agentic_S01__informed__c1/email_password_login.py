import requests
from identity_client import get_firebase_web_api_key
from identity_models import LoginRequest, LoginResponse


def email_password_login(login_request: LoginRequest) -> LoginResponse:
    """
    Signs in a user with email and password using Firebase Auth REST API.
    """
    api_key = get_firebase_web_api_key()
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

    payload = {
        "email": login_request.email,
        "password": login_request.password,
        "returnSecureToken": True,
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()  # Raises an exception for bad status codes
    data = response.json()

    return LoginResponse(
        id_token=data["idToken"],
        refresh_token=data["refreshToken"],
        expires_in=int(data["expiresIn"]),
        local_id=data["localId"],
    )
