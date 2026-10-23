import os
import requests
from identity_models import PasswordResetRequest
from identity_client import FIREBASE_IDENTITY_TOOLKIT_URL, get_firebase_api_key

def password_reset(reset_request: PasswordResetRequest) -> dict:
    api_key = get_firebase_api_key()
    endpoint = f"{FIREBASE_IDENTITY_TOOLKIT_URL}:sendOobCode?key={api_key}"
    payload = {
        "requestType": "PASSWORD_RESET",
        "email": reset_request.email
    }
    response = requests.post(endpoint, json=payload)
    response.raise_for_status()
    return response.json()
