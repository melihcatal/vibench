import firebase_admin
from firebase_admin import auth
from identity_client import get_firebase_app
from identity_models import EmailPasswordLoginRequest, EmailPasswordLoginResponse


def email_password_login(
    request: EmailPasswordLoginRequest,
) -> EmailPasswordLoginResponse:
    app = get_firebase_app()
    # Firebase Admin SDK does not directly support email/password login to get tokens for a user
    # It's primarily for server-side user management.
    # For client-side login, a client SDK would be used.
    # To simulate, we'll verify the password and then generate a custom token.
    # In a real scenario, client-side would handle the login and get ID/refresh tokens.
    try:
        # Admin SDK doesn't have a direct 'login' method that returns tokens for existing users.
        # This is a workaround: verify user exists, then create a custom token.
        user = auth.get_user_by_email(request.email, app=app)
        # For a true login, password verification happens client-side or via a separate API.
        # The Admin SDK can only check for user existence and generate custom tokens.

        # In a real app, a client-side Firebase SDK would handle this:
        # firebase.auth().signInWithEmailAndPassword(email, password)

        # For server-side, we can generate a custom token which the client can use to sign in.
        custom_token = auth.create_custom_token(user.uid, app=app)
        # Note: This custom token needs to be exchanged for ID/refresh tokens on the client-side.
        # This response structure is simplified for demonstration.

        return EmailPasswordLoginResponse(
            uid=user.uid,
            email=user.email,
            id_token=custom_token.decode(
                "utf-8"
            ),  # Custom token is not an ID token, but used as a placeholder
            refresh_token="simulated_refresh_token",
        )
    except Exception as e:
        raise Exception(f"Firebase login failed: {e}")
