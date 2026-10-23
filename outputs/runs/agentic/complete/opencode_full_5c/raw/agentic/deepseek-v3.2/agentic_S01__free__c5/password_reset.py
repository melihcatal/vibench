import requests
import os
from identity_models import PasswordResetRequest, PasswordResetResponse


def password_reset(email: str) -> PasswordResetResponse:
    """Start a password reset flow for a local account using Firebase Authentication."""
    try:
        # Firebase API key from environment
        api_key = os.environ.get("FIREBASE_API_KEY")
        if not api_key:
            raise ValueError("FIREBASE_API_KEY environment variable is required")

        # Firebase password reset endpoint
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={api_key}"

        # Prepare reset request
        payload = {"requestType": "PASSWORD_RESET", "email": email}

        # Make API call to Firebase
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

        # Check if email was sent
        email_sent = data.get("email", "") == email

        # Return normalized response
        return PasswordResetResponse(
            email=email,
            reset_initiated=email_sent,
            reset_link_sent=True,
            provider="firebase",
            message="Password reset email sent"
            if email_sent
            else "Password reset failed",
        )
    except requests.exceptions.RequestException as e:
        if e.response and e.response.status_code == 400:
            error_data = e.response.json()
            error_msg = error_data.get("error", {}).get(
                "message", "Password reset failed"
            )
            if "EMAIL_NOT_FOUND" in error_msg:
                # For security, don't reveal if email exists or not
                return PasswordResetResponse(
                    email=email,
                    reset_initiated=False,
                    reset_link_sent=False,
                    provider="firebase",
                    message="If this email exists in our system, a reset link has been sent",
                )
        raise RuntimeError(f"Password reset failed: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Password reset failed: {str(e)}")
