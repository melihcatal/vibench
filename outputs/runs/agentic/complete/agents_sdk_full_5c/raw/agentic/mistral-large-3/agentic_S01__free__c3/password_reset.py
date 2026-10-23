import os
import requests
from identity_models import PasswordResetRequest, PasswordResetResponse, PasswordResetError


def password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    firebase_api_key = os.getenv("FIREBASE_API_KEY")
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={firebase_api_key}"

    payload = {
        "requestType": "PASSWORD_RESET",
        "email": request.email
    }

    response = requests.post(url, json=payload)
    data = response.json()

    if response.status_code == 200:
        return PasswordResetResponse(
            success=True,
            email=request.email
        )
    else:
        return PasswordResetResponse(
            success=False,
            error=PasswordResetError(
                code=data.get("error", {}).get("code"),
                message=data.get("error", {}).get("message")
            )
        )