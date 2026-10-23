import firebase_admin
from firebase_admin import auth, credentials
import requests # For calling the Firebase REST API directly for sign-in

# Firebase project configuration (replace with your actual values)
# For client-side sign-in, you typically use a web API key.
# This example uses a simplified approach for demonstration, usually you'd use client SDKs.
FIREBASE_WEB_API_KEY = "YOUR_FIREBASE_WEB_API_KEY" # e.g., from Firebase Project Settings -> General -> Web API Key
FIREBASE_AUTH_SIGNIN_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"

# Initialize Firebase Admin SDK if not already initialized
# This is mainly for server-side operations, not direct client sign-in with email/password.
if not firebase_admin._apps:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)

def email_password_login(email: str, password: str) -> dict:
    """
    Signs in a user with email and password using Firebase Authentication REST API
    and returns ID and refresh tokens.
    """
    try:
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(FIREBASE_AUTH_SIGNIN_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        return {
            "idToken": data.get("idToken"),
            "refreshToken": data.get("refreshToken"),
            "expiresIn": data.get("expiresIn"),
            "localId": data.get("localId"),
            "message": "User signed in successfully."
        }
    except requests.exceptions.HTTPError as e:
        error_data = e.response.json()
        return {"error": error_data.get("error", {}).get("message", str(e))}
    except Exception as e:
        return {"error": str(e)}
