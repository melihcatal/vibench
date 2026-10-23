import os
from firebase_admin import auth
from identity_client import initialize_firebase
from identity_models import PasswordResetRequest, PasswordResetResponse

# Initialize Firebase Admin SDK (if not already initialized)
initialize_firebase()


def password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    """Initiates a password reset flow by sending a password reset email to the user."""
    try:
        # Ensure the user exists before attempting to send a reset email
        auth.get_user_by_email(request.email)
        link = auth.generate_password_reset_link(request.email)
        # In a real application, you might log this link or send it via a custom email service.
        # For this example, we just confirm the link generation.
        return PasswordResetResponse(
            message=f"Password reset link generated and conceptually sent to {request.email}. Link: {link}"
        )
    except auth.UserNotFoundError:
        raise ValueError(f"User with email {request.email} not found.")
    except Exception as e:
        raise ValueError(f"Failed to initiate password reset: {e}")
