import requests
import os
from identity_models import UserLoginRequest

FIREBASE_WEB_API_KEY = os.environ.get("FIREBASE_WEB_API_KEY")
FIREBASE_AUTH_SIGN_IN_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"

def email_password_login(login_request: UserLoginRequest):
    """
    Signs in a user with email and password using Firebase Authentication REST API
    and returns ID and refresh tokens.
    """
    if not FIREBASE_WEB_API_KEY:
        return {"error": "FIREBASE_WEB_API_KEY environment variable not set."}

    payload = {
        "email": login_request.email,
        "password": login_request.password,
        "returnSecureToken": True
    }

    try:
        response = requests.post(FIREBASE_AUTH_SIGN_IN_URL, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return {
            "idToken": data.get("idToken"),
            "refreshToken": data.get("refreshToken"),
            "expiresIn": data.get("expiresIn"),
            "email": data.get("email"),
            "localId": data.get("localId"),
            "message": "User logged in successfully"
        }
    except requests.exceptions.HTTPError as e:
        error_data = e.response.json()
        return {"error": error_data.get("error", {}).get("message", str(e))}
    except Exception as e:
        return {"error": str(e)}
