import os
import requests
from identity_models import RefreshSessionRequest, RefreshSessionResponse

# Firebase Web API Key for client-side authentication.
FIREBASE_WEB_API_KEY = os.environ.get("FIREBASE_WEB_API_KEY")
FIREBASE_AUTH_REFRESH_API = "https://securetoken.googleapis.com/v1/token"

def refresh_session(request: RefreshSessionRequest) -> RefreshSessionResponse:
    if not FIREBASE_WEB_API_KEY:
        raise ValueError("FIREBASE_WEB_API_KEY not set.")

    url = f"{FIREBASE_AUTH_REFRESH_API}?key={FIREBASE_WEB_API_KEY}"
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": request.refresh_token
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        return RefreshSessionResponse(
            id_token=data.get("id_token"),
            refresh_token=data.get("refresh_token"), # Firebase sometimes returns a new refresh token
            expires_in=data.get("expires_in"),
            user_id=data.get("user_id")
        )
    except requests.exceptions.HTTPError as e:
        error_data = e.response.json()
        error_message = error_data.get("error", {}).get("message", "Unknown error")
        raise RuntimeError(f"Firebase session refresh failed: {error_message} (Status: {e.response.status_code})")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred during session refresh: {e}")
