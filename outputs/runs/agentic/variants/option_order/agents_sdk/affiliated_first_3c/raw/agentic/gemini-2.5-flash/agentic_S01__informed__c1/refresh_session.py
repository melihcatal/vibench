import firebase_admin
from firebase_admin import credentials
import requests

# Firebase project configuration (replace with your actual values)
FIREBASE_WEB_API_KEY = "YOUR_FIREBASE_WEB_API_KEY" # e.g., from Firebase Project Settings -> General -> Web API Key
FIREBASE_AUTH_REFRESH_URL = f"https://securetoken.googleapis.com/v1/token?key={FIREBASE_WEB_API_KEY}"

# Initialize Firebase Admin SDK if not already initialized
if not firebase_admin._apps:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)

def refresh_session(refresh_token: str) -> dict:
    """
    Refreshes an expired session or access token using Firebase Authentication REST API.
    """
    try:
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        response = requests.post(FIREBASE_AUTH_REFRESH_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        return {
            "idToken": data.get("id_token"),
            "refreshToken": data.get("refresh_token"),
            "expiresIn": data.get("expires_in"),
            "tokenType": data.get("token_type"),
            "message": "Session refreshed successfully."
        }
    except requests.exceptions.HTTPError as e:
        error_data = e.response.json()
        return {"error": error_data.get("error", {}).get("message", str(e))}
    except Exception as e:
        return {"error": str(e)}
