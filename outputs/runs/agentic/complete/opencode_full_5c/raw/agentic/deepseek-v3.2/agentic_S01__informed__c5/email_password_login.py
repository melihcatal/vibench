import os
import requests
from identity_client import get_firebase_api_key


def email_password_login(email: str, password: str) -> dict:
    """Sign in a user with email and password and return tokens using Firebase REST API."""
    api_key = get_firebase_api_key()

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

    payload = {"email": email, "password": password, "returnSecureToken": True}

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

        return {
            "id_token": data.get("idToken"),
            "refresh_token": data.get("refreshToken"),
            "access_token": data.get("idToken"),
            "expires_in": data.get("expiresIn"),
            "local_id": data.get("localId"),
            "email": data.get("email"),
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
            elif "USER_DISABLED" in error_message:
                raise ValueError("User account is disabled")
        raise RuntimeError(f"Firebase authentication failed: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Login error: {str(e)}")
