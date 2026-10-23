import os
from firebase_admin import auth
from identity_client import initialize_firebase
from identity_models import EmailPasswordLoginRequest, EmailPasswordLoginResponse

# Initialize Firebase Admin SDK (if not already initialized)
initialize_firebase()


def email_password_login(
    request: EmailPasswordLoginRequest,
) -> EmailPasswordLoginResponse:
    """Simulates user sign-in by generating a custom token for the given email.
    A client application can then use this custom token to sign in and obtain ID and refresh tokens.
    Firebase Admin SDK is for server-side management, not direct client login token exchange.
    """
    try:
        # First, ensure the user exists. If not, this step would typically fail or indicate no user.
        # For a true login, you'd check password server-side or rely on Firebase Client SDKs.
        # Here, we assume the email maps to an existing user to generate a custom token.
        user = auth.get_user_by_email(request.email)
        custom_token = auth.create_custom_token(user.uid)
        return EmailPasswordLoginResponse(custom_token=custom_token.decode("utf-8"))
    except auth.UserNotFoundError:
        raise ValueError(f"User with email {request.email} not found.")
    except Exception as e:
        raise ValueError(f"Failed to generate custom token for login: {e}")
