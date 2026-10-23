import requests
import json
from identity_client import get_firebase_api_key
from identity_models import UserCredentials, LoginResponse

# Firebase Authentication REST API endpoint for signing in with email/password
FIREBASE_SIGN_IN_URL = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

def login_with_email_password(credentials: UserCredentials) -> LoginResponse:
    """
    Signs in a user with email and password using Firebase REST API.

    Args:
        credentials: User's email and password.

    Returns:
        A LoginResponse object with tokens.
    """
    api_key = get_firebase_api_key()
    payload = {
        "email": credentials.email,
        "password": credentials.password,
        "returnSecureToken": True
    }
    params = {"key": api_key}
    
    response = requests.post(FIREBASE_SIGN_IN_URL, params=params, json=payload)
    response.raise_for_status()  # Raise an exception for HTTP errors
    
    data = response.json()
    return LoginResponse(
        id_token=data['idToken'],
        refresh_token=data['refreshToken'],
        expires_in=data['expiresIn'],
        local_id=data['localId']
    )
