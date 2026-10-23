import requests
import os

FIREBASE_WEB_API_KEY = os.environ.get("FIREBASE_WEB_API_KEY")
FIREBASE_AUTH_TOKEN_REFRESH_URL = f"https://securetoken.googleapis.com/v1/token?key={FIREBASE_WEB_API_KEY}"

def refresh_session(refresh_token: str):
    """
    Refreshes an expired session or access token using Firebase Authentication REST API.
    """
    if not FIREBASE_WEB_API_KEY:
        return {"error": "FIREBASE_WEB_API_KEY environment variable not set."}

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    try:
        response = requests.post(FIREBASE_AUTH_TOKEN_REFRESH_URL, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return {
            "id_token": data.get("id_token"),
            "refresh_token": data.get("refresh_token"),
            "expires_in": data.get("expires_in"),
            "message": "Session refreshed successfully"
        }
    except requests.exceptions.HTTPError as e:
        error_data = e.response.json()
        return {"error": error_data.get("error", {}).get("message", str(e))}
    except Exception as e:
        return {"error": str(e)}
