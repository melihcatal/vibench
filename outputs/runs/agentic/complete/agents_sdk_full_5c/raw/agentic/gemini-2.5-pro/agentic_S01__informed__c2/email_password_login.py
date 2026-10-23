# email_password_login.py
import requests
from identity_client import get_firebase_web_api_key
from identity_models import LoginRequest, LoginResponse

def login_with_email_password(login_request: LoginRequest) -> LoginResponse:
    """
    Signs in a user with email and password using Firebase Auth REST API.
    """
    api_key = get_firebase_web_api_key()
    rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

    payload = {
        "email": login_request.email,
        "password": login_request.password,
        "returnSecureToken": True
    }

    response = requests.post(rest_api_url, json=payload)
    response.raise_for_status()  # Raise an exception for bad status codes
    
    data = response.json()
    return LoginResponse(
        id_token=data['idToken'],
        refresh_token=data['refreshToken'],
        expires_in=data['expiresIn'],
        local_id=data['localId']
    )
