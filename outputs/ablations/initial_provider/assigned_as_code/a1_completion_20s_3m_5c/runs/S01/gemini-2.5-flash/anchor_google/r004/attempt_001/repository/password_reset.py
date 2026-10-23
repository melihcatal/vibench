import requests
from identity_models import PasswordResetPayload
from typing import Dict, Any


def password_reset(payload: PasswordResetPayload, config: Dict[str, Any]):
    api_key = config["firebase_web_api_key"]
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {"requestType": "PASSWORD_RESET", "email": payload.email}

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    return {"message": "Password reset email sent"}
