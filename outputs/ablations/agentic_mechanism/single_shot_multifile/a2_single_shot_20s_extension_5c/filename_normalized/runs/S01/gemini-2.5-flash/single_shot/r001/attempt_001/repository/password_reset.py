import os
import requests
from identity_models import PasswordResetRequest, PasswordResetResponse

FIREBASE_WEB_API_KEY = os.environ.get("FIREBASE_WEB_API_KEY")
if not FIREBASE_WEB_API_KEY:
    raise EnvironmentError("FIREBASE_WEB_API_KEY environment variable not set.")

FIREBASE_PASSWORD_RESET_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={FIREBASE_WEB_API_KEY}"

def initiate_password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    payload = {
        "requestType": "PASSWORD_RESET",
        "email": request.email
    }
    response = requests.post(FIREBASE_PASSWORD_RESET_URL, json=payload)
    response.raise_for_status()
    data = response.json()

    return PasswordResetResponse(
        email=data["email"],
        kind=data["kind"]
    )