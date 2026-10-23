import os
import requests
from identity_models import UserCredentials, LoginResponse
from identity_client import FIREBASE_IDENTITY_TOOLKIT_URL, get_firebase_api_key

def register_user(credentials: UserCredentials) -> LoginResponse:
    api_key = get_firebase_api_key()
    endpoint = f"{FIREBASE_IDENTITY_TOOLKIT_URL}:signUp?key={api_key}"
    payload = {
        "email": credentials.email,
        "password": credentials.password,
        "returnSecureToken": True
    }
    response = requests.post(endpoint, json=payload)
    response.raise_for_status()
    return LoginResponse(**response.json())
