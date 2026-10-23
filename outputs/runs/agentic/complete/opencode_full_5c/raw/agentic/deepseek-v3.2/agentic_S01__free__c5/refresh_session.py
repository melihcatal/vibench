import requests
import os
from identity_models import RefreshRequest, RefreshResponse


def refresh_session(refresh_token: str) -> RefreshResponse:
    """Refresh an expired session or access token using Firebase Authentication."""
    try:
        # Firebase API key from environment
        api_key = os.environ.get("FIREBASE_API_KEY")
        if not api_key:
            raise ValueError("FIREBASE_API_KEY environment variable is required")

        # Firebase token refresh endpoint
        url = f"https://securetoken.googleapis.com/v1/token?key={api_key}"

        # Prepare refresh request
        payload = {"grant_type": "refresh_token", "refresh_token": refresh_token}

        # Make API call to Firebase
        response = requests.post(url, data=payload)
        response.raise_for_status()
        data = response.json()

        # Extract new tokens
        id_token = data.get("id_token")
        new_refresh_token = data.get("refresh_token")
        user_id = data.get("user_id")

        if not id_token:
            raise ValueError("No new access token received from Firebase")

        # Return normalized response
        return RefreshResponse(
            user_id=user_id,
            access_token=id_token,
            refresh_token=new_refresh_token or refresh_token,
            expires_in=data.get("expires_in", 3600),
            token_type=data.get("token_type", "Bearer"),
            provider="firebase",
        )
    except requests.exceptions.RequestException as e:
        if e.response and e.response.status_code == 400:
            error_data = e.response.json()
            error_msg = error_data.get("error", {}).get(
                "message", "Invalid refresh token"
            )
            if "TOKEN_EXPIRED" in error_msg or "INVALID_REFRESH_TOKEN" in error_msg:
                raise ValueError("Refresh token is invalid or expired")
        raise RuntimeError(f"Token refresh failed: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Token refresh failed: {str(e)}")
