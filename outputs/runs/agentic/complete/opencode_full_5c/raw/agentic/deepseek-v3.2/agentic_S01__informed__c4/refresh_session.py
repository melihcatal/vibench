import os
import requests
import json


def refresh_session(refresh_token: str) -> dict:
    """
    Refresh an expired session or access token using Firebase Authentication REST API.
    """
    api_key = os.getenv("FIREBASE_API_KEY")
    if not api_key:
        raise ValueError("FIREBASE_API_KEY environment variable not set")

    url = f"https://securetoken.googleapis.com/v1/token?key={api_key}"

    payload = {"grant_type": "refresh_token", "refresh_token": refresh_token}

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        data = response.json()

        return {
            "id_token": data.get("id_token"),
            "refresh_token": data.get("refresh_token"),
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
            else:
                raise ValueError(f"Token refresh error: {error_message}")
        raise RuntimeError(f"Token refresh failed: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Token refresh failed: {str(e)}")
