import os
import requests
from identity_models import PasswordResetRequest, PasswordResetResponse

def password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    firebase_api_key = os.environ.get("FIREBASE_API_KEY")
    if not firebase_api_key:
        raise ValueError("FIREBASE_API_KEY environment variable not set.")

    rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={firebase_api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "requestType": "PASSWORD_RESET",
        "email": request.email,
    }

    response = requests.post(rest_api_url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()

    return PasswordResetResponse(email=data.get("email"))
