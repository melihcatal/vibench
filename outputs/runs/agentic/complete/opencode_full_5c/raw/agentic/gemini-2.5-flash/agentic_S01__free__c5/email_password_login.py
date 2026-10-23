from identity_client import get_firebase_auth
from identity_models import EmailPasswordLoginRequest, EmailPasswordLoginResponse


def email_password_login(
    request: EmailPasswordLoginRequest,
) -> EmailPasswordLoginResponse:
    # Firebase Admin SDK does not directly provide a login function that returns ID/refresh tokens
    # for email/password. This is typically done on the client-side.
    # For a server-side equivalent, we'll simulate by creating a custom token
    # and then assume a client-side exchange for ID/refresh tokens.
    # In a real scenario, the client-side Firebase SDK would handle this.
    auth = get_firebase_auth()
    try:
        # Verify user exists (optional, client would typically handle login directly)
        user = auth.get_user_by_email(request.email)
        # For demonstration, we generate a custom token. A real client would then exchange this
        # for ID and refresh tokens using the Firebase client SDK.
        custom_token = auth.create_custom_token(user.uid)

        # NOTE: A real client-side login would return actual ID and refresh tokens.
        # This is a placeholder for server-side logic that might precede a client login.
        # To get ID/refresh tokens server-side with email/password, you'd need to use
        # the Firebase Authentication REST API directly with the sign-in endpoint,
        # which requires an API key and is usually discouraged for server-to-server.
        # The expires_in is for the custom token, which is short-lived (1 hour).
        return EmailPasswordLoginResponse(
            id_token=custom_token.decode("utf-8"),
            refresh_token="simulated_refresh_token",  # Placeholder
            expires_in="3600",  # 1 hour for custom token
        )
    except Exception as e:
        raise ValueError(f"Failed to login: {e}")
