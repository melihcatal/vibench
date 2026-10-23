import os
import requests
import json


def email_password_login(email: str, password: str) -> dict:
    """
    Sign in a user with email and password using Firebase Authentication REST API.
    Returns ID token, refresh token, and user info.
    """
    api_key = os.getenv("FIREBASE_API_KEY")
    if not api_key:
        raise ValueError("FIREBASE_API_KEY environment variable not set")

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

    payload = {"email": email, "password": password, "returnSecureToken": True}

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()

        return {
            "id_token": data.get("idToken"),
            "refresh_token": data.get("refreshToken"),
            "expires_in": data.get("expiresIn"),
            "local_id": data.get("localId"),
            "email": data.get("email"),
            "display_name": data.get("displayName"),
            "provider": "firebase",
        }
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            error_data = e.response.json()
            error_message = error_data.get("error", {}).get(
                "message", "Authentication failed"
            )
            if (
                "INVALID_PASSWORD" in error_message
                or "EMAIL_NOT_FOUND" in error_message
            ):
                raise ValueError("Invalid email or password")
            else:
                raise ValueError(f"Authentication error: {error_message}")
        raise RuntimeError(f"Login failed: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Login failed: {str(e)}")
