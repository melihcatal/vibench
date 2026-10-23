import requests
from identity_client import FIREBASE_WEB_API_KEY
from identity_models import password_reset_request

FIREBASE_PASSWORD_RESET_API_URL = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key=" + FIREBASE_WEB_API_KEY

def password_reset(email):
    """
    Starts a password reset flow for a local account using Firebase Authentication REST API.
    An email will be sent to the user with instructions to reset their password.
    """
    payload = password_reset_request(email)
    try:
        response = requests.post(FIREBASE_PASSWORD_RESET_API_URL, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return {"email": email, "message": "Password reset email sent successfully."}
    except requests.exceptions.RequestException as e:
        error_message = response.json().get("error", {}).get("message", str(e))
        return {"error": error_message, "message": "Failed to send password reset email."}
