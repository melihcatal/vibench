import os
import requests
from identity_client import FIREBASE_IDENTITY_TOOLKIT_URL, get_api_key
from identity_models import PasswordResetRequest, PasswordResetResponse

def password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    api_key = get_api_key()
    url = f"{FIREBASE_IDENTITY_TOOLKIT_URL}sendOobCode?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "requestType": "PASSWORD_RESET",
        "email": request["email"]
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()

    return {
        "email": data["email"]
    }