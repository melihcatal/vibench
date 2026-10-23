import requests
import os
from identity_models import PasswordResetPayload

def password_reset(payload: PasswordResetPayload):
    api_key = os.getenv("FIREBASE_WEB_API_KEY")
    if not api_key:
        raise ValueError("FIREBASE_WEB_API_KEY environment variable not set.")

    rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "requestType": "PASSWORD_RESET",
        "email": payload.email
    }

    response = requests.post(rest_api_url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()
