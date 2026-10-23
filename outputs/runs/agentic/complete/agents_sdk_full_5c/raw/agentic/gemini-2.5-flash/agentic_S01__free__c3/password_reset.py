import os
import requests
from identity_models import PasswordResetRequest, PasswordResetResponse

# Firebase Auth REST API Endpoint for sending password reset emails
FIREBASE_WEB_API_KEY = os.environ.get("FIREBASE_WEB_API_KEY")
FIREBASE_AUTH_PASSWORD_RESET_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={FIREBASE_WEB_API_KEY}"

def password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    if not FIREBASE_WEB_API_KEY:
        raise ValueError("FIREBASE_WEB_API_KEY environment variable is not set.")

    payload = {
        "requestType": "PASSWORD_RESET",
        "email": request.email
    }
    try:
        response = requests.post(FIREBASE_AUTH_PASSWORD_RESET_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        return PasswordResetResponse(email=data.get("email"))
    except requests.exceptions.HTTPError as e:
        error_message = e.response.json().get("error", {}).get("message", "Unknown error")
        raise RuntimeError(f"Failed to send password reset email: {error_message}") from e
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred during password reset initiation: {e}")

if __name__ == '__main__':
    # This block is for demonstration/testing only
    # os.environ["FIREBASE_WEB_API_KEY"] = "YOUR_FIREBASE_WEB_API_KEY"
    # try:
    #     reset_req = PasswordResetRequest(email="test@example.com")
    #     reset_res = password_reset(reset_req)
    #     print(f"Password reset email sent to: {reset_res.email}")
    # except RuntimeError as e:
    #     print(f"Password reset error: {e}")
    pass
