import requests
import os

FIREBASE_WEB_API_KEY = os.environ.get("FIREBASE_WEB_API_KEY")
FIREBASE_AUTH_PASSWORD_RESET_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={FIREBASE_WEB_API_KEY}"

def password_reset(email: str):
    """
    Starts a password reset flow for an account using Firebase Authentication REST API.
    An email will be sent to the user with a password reset link.
    """
    if not FIREBASE_WEB_API_KEY:
        return {"error": "FIREBASE_WEB_API_KEY environment variable not set."}

    payload = {
        "requestType": "PASSWORD_RESET",
        "email": email
    }

    try:
        response = requests.post(FIREBASE_AUTH_PASSWORD_RESET_URL, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return {"email": data.get("email"), "message": "Password reset email sent successfully."}
    except requests.exceptions.HTTPError as e:
        error_data = e.response.json()
        return {"error": error_data.get("error", {}).get("message", str(e))}
    except Exception as e:
        return {"error": str(e)}
