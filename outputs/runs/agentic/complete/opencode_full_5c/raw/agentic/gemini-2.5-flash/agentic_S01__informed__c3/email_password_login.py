from identity_client import get_auth_client
from identity_models import EmailPasswordLoginRequest, EmailPasswordLoginResponse


def email_password_login(
    request: EmailPasswordLoginRequest,
) -> EmailPasswordLoginResponse:
    # Firebase Admin SDK does not provide a direct email/password login method that returns tokens.
    # This is typically handled client-side using Firebase Client SDKs (e.g., JavaScript, Android, iOS).
    # For the purpose of this simulation, we'll validate the user exists and return simulated tokens.
    # In a real scenario, this would involve a client-side call to get actual ID and refresh tokens.

    auth = get_auth_client()
    try:
        user = auth.get_user_by_email(request.email)
        # Simulate successful login and token generation
        return EmailPasswordLoginResponse(
            uid=user.uid,
            email=user.email,
            id_token="simulated_firebase_id_token",
            refresh_token="simulated_firebase_refresh_token",
        )
    except Exception as e:
        raise ValueError(
            f"Firebase login failed: {e}. In a real app, integrate client-side Firebase Auth for login and token retrieval."
        )
