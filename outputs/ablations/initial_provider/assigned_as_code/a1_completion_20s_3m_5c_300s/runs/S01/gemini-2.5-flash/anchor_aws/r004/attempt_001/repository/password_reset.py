from identity_client import get_firebase_client
from identity_models import PasswordResetRequest
import requests
import os

def password_reset(request: PasswordResetRequest):
    api_key = os.environ.get("FIREBASE_API_KEY")
    rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={api_key}"
    payload = {
        "requestType": "PASSWORD_RESET",
        "email": request.email
    }
    response = requests.post(rest_api_url, json=payload).json()
    if "error" in response:
        raise Exception(response["error"]["message"])
    return {"message": f"Password reset email sent to {request.email}"}
