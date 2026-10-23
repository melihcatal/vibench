import os
import requests
from identity_client import get_firebase_api_key


def password_reset(email: str) -> dict:
    """Start a password reset flow for a local account using Firebase REST API."""
    api_key = get_firebase_api_key()

    url = (
        f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={api_key}"
    )

    payload = {"requestType": "PASSWORD_RESET", "email": email}

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

        return {
            "email": data.get("email"),
            "request_type": "PASSWORD_RESET",
            "success": True,
            "message": "Password reset email sent successfully",
            "provider": "firebase",
        }
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            error_data = e.response.json()
            error_message = error_data.get("error", {}).get(
                "message", "Password reset failed"
            )
            if "EMAIL_NOT_FOUND" in error_message:
                raise ValueError(f"No user found with email {email}")
            elif "TOO_MANY_ATTEMPTS_TRY_LATER" in error_message:
                raise ValueError("Too many attempts. Please try again later.")
        raise RuntimeError(f"Password reset failed: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Password reset error: {str(e)}")
