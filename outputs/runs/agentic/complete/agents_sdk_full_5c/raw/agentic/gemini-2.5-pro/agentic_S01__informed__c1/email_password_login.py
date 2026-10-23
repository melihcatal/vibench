import requests
import os
from identity_client import get_firebase_api_key
from identity_models import UserLoginRequest, UserLoginResponse

def sign_in_with_password(login_request: UserLoginRequest) -> UserLoginResponse:
    """
    Signs in a user with email and password using Firebase Auth REST API.
    The Admin SDK does not support signing users in directly with passwords.
    """
    api_key = get_firebase_api_key()
    rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

    payload = {
        "email": login_request.email,
        "password": login_request.password,
        "returnSecureToken": True
    }

    response = requests.post(rest_api_url, json=payload, timeout=10)
    response.raise_for_status() # Raises an exception for 4XX/5XX errors

    data = response.json()
    return UserLoginResponse.model_validate(data)
