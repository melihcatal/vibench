import firebase_admin
from firebase_admin import auth, credentials
import requests

# Firebase project configuration (replace with your actual values)
FIREBASE_WEB_API_KEY = "YOUR_FIREBASE_WEB_API_KEY" # e.g., from Firebase Project Settings -> General -> Web API Key
FIREBASE_AUTH_RESET_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={FIREBASE_WEB_API_KEY}"

# Initialize Firebase Admin SDK if not already initialized
if not firebase_admin._apps:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)

def password_reset(email: str) -> dict:
    """
    Starts a password reset flow for a local account using Firebase Authentication.
    """
    try:
        payload = {
            "requestType": "PASSWORD_RESET",
            "email": email
        }
        response = requests.post(FIREBASE_AUTH_RESET_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        return {"email": data.get("email"), "message": "Password reset email sent successfully."}
    except requests.exceptions.HTTPError as e:
        error_data = e.response.json()
        return {"error": error_data.get("error", {}).get("message", str(e))}
    except Exception as e:
        return {"error": str(e)}
