import requests
from identity_client import get_firebase_api_key
from identity_models import UserLoginRequest, AuthResponse

def login(credentials: UserLoginRequest) -> AuthResponse:
    """
    Signs in a user with email and password using Firebase Auth REST API.
    """
    api_key = get_firebase_api_key()
    
    # Firebase Authentication REST API endpoint for signing in with password
    rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

    payload = {
        "email": credentials.email,
        "password": credentials.password,
        "returnSecureToken": True
    }

    response = requests.post(rest_api_url, json=payload)
    response.raise_for_status()  # Raise an exception for bad status codes

    auth_data = response.json()
    return AuthResponse.model_validate(auth_data)
