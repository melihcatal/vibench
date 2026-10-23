import os
import requests
from identity_models import PasswordResetRequest, PasswordResetResponse


def password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    try:
        # Firebase REST API for password reset
        rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={os.getenv('FIREBASE_API_KEY')}"
        payload = {
            "requestType": "PASSWORD_RESET",
            "email": request.email
        }
        response = requests.post(rest_api_url, json=payload)
        response.raise_for_status()
        
        return PasswordResetResponse(
            success=True,
            email=request.email
        )
    except requests.exceptions.RequestException as e:
        return PasswordResetResponse(
            success=False,
            error_message=str(e)
        )