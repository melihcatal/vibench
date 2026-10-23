import os
import requests
from identity_models import PasswordResetRequest, PasswordResetResponse

# Firebase Web API Key.
FIREBASE_WEB_API_KEY = os.environ.get("FIREBASE_WEB_API_KEY")
FIREBASE_AUTH_REST_API = "https://identitytoolkit.googleapis.com/v1/accounts"

def password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    if not FIREBASE_WEB_API_KEY:
        raise ValueError("FIREBASE_WEB_API_KEY not set.")

    url = f"{FIREBASE_AUTH_REST_API}:sendOobCode?key={FIREBASE_WEB_API_KEY}"
    payload = {
        "requestType": "PASSWORD_RESET",
        "email": request.email
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Firebase returns the email if successful.
        return PasswordResetResponse(email=data.get("email"))
    except requests.exceptions.HTTPError as e:
        error_data = e.response.json()
        error_message = error_data.get("error", {}).get("message", "Unknown error")
        raise RuntimeError(f"Firebase password reset failed: {error_message} (Status: {e.response.status_code})")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred during password reset: {e}")
