import os
import requests
from identity_client import get_firebase_api_key


def refresh_session(refresh_token: str) -> dict:
    """Refresh an expired session or access token using Firebase REST API."""
    api_key = get_firebase_api_key()

    url = f"https://securetoken.googleapis.com/v1/token?key={api_key}"

    payload = {"grant_type": "refresh_token", "refresh_token": refresh_token}

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

        return {
            "id_token": data.get("id_token"),
            "refresh_token": data.get("refresh_token"),
            "access_token": data.get("id_token"),
            "expires_in": data.get("expires_in"),
            "token_type": data.get("token_type"),
            "user_id": data.get("user_id"),
            "project_id": data.get("project_id"),
            "provider": "firebase",
        }
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            error_data = e.response.json()
            error_message = error_data.get("error", {}).get(
                "message", "Token refresh failed"
            )
            if (
                "TOKEN_EXPIRED" in error_message
                or "INVALID_REFRESH_TOKEN" in error_message
            ):
                raise ValueError("Invalid or expired refresh token")
        raise RuntimeError(f"Token refresh failed: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Refresh error: {str(e)}")
