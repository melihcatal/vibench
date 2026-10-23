import requests
from identity_models import PasswordResetRequest, PasswordResetResponse
import os


def password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    reset_url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={os.getenv('FIREBASE_API_KEY')}"
    payload = {"requestType": "PASSWORD_RESET", "email": request.email}
    response = requests.post(reset_url, json=payload)

    if response.status_code == 200:
        return PasswordResetResponse(success=True, email=request.email)
    else:
        return PasswordResetResponse(
            success=False,
            error=response.json()
            .get("error", {})
            .get("message", "Password reset failed"),
        )
