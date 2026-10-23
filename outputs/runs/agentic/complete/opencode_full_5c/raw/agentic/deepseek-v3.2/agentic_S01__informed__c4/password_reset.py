import os
import requests
import json


def password_reset(email: str) -> dict:
    """
    Start a password reset flow for a local account using Firebase Authentication REST API.
    """
    api_key = os.getenv("FIREBASE_API_KEY")
    if not api_key:
        raise ValueError("FIREBASE_API_KEY environment variable not set")

    url = (
        f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={api_key}"
    )

    payload = {"requestType": "PASSWORD_RESET", "email": email}

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
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
                raise ValueError("Email not found")
            else:
                raise ValueError(f"Password reset error: {error_message}")
        raise RuntimeError(f"Password reset failed: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Password reset failed: {str(e)}")
