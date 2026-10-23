import os
import requests
from identity_models import RefreshSessionRequest, RefreshSessionResponse

# Firebase Auth REST API Endpoint for refreshing ID tokens
# The Firebase Admin SDK does not directly provide a simple method to refresh a client-side ID token
# using the refresh token, so we rely on the REST API.
FIREBASE_WEB_API_KEY = os.environ.get("FIREBASE_WEB_API_KEY")
FIREBASE_AUTH_REFRESH_TOKEN_URL = f"https://securetoken.googleapis.com/v1/token?key={FIREBASE_WEB_API_KEY}"

def refresh_session(request: RefreshSessionRequest) -> RefreshSessionResponse:
    if not FIREBASE_WEB_API_KEY:
        raise ValueError("FIREBASE_WEB_API_KEY environment variable is not set.")

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": request.refresh_token
    }
    try:
        response = requests.post(FIREBASE_AUTH_REFRESH_TOKEN_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        return RefreshSessionResponse(
            id_token=data.get("id_token"),
            refresh_token=data.get("refresh_token") or request.refresh_token, # Refresh token might not change
            expires_in=int(data.get("expires_in", 0)),
            uid=data.get("user_id")
        )
    except requests.exceptions.HTTPError as e:
        error_message = e.response.json().get("error", {}).get("message", "Unknown error")
        raise RuntimeError(f"Failed to refresh session: {error_message}") from e
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred during session refresh: {e}")

if __name__ == '__main__':
    # This block is for demonstration/testing only
    # os.environ["FIREBASE_WEB_API_KEY"] = "YOUR_FIREBASE_WEB_API_KEY"
    # Placeholder refresh token (obtained from a login)
    # refresh_token = "YOUR_USERS_REFRESH_TOKEN"
    # try:
    #     refresh_req = RefreshSessionRequest(refresh_token=refresh_token)
    #     refresh_res = refresh_session(refresh_req)
    #     print(f"Session refreshed. New ID Token (truncated): {refresh_res.id_token[:30]}...")
    # except RuntimeError as e:
    #     print(f"Refresh error: {e}")
    pass
