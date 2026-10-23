import requests
from identity_client import get_firebase_api_key
from identity_models import PasswordResetRequest, PasswordResetResponse

FIREBASE_AUTH_RESET_URL = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key="

def password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    api_key = get_firebase_api_key()
    url = f"{FIREBASE_AUTH_RESET_URL}{api_key}"
    payload = {
        "requestType": "PASSWORD_RESET",
        "email": request.email
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()
    return PasswordResetResponse(email=data["email"])
