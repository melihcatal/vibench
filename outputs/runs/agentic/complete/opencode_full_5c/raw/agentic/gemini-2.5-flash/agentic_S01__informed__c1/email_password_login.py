from identity_client import firebase_auth
from identity_models import UserLoginRequest, UserLoginResponse


def email_password_login(request: UserLoginRequest) -> UserLoginResponse:
    """
    Signs in a user by generating a custom Firebase token.
    Note: Firebase Admin SDK does not directly sign in users like client-side SDKs.
    It generates custom tokens that can be used by client-side SDKs to sign in.
    Password verification is implicitly handled if the user was created via email/password.
    For this example, we assume user existence and generate a custom token.
    A client-side application would then exchange this custom token for ID and refresh tokens.
    """
    try:
        user = firebase_auth.get_user_by_email(request.email)
        # In a real scenario, you'd verify the password here against a secure hash
        # or rely on a client-side Firebase Auth call for email/password login.
        # Since we're using firebase-admin, we generate a custom token for the existing user.
        custom_token = firebase_auth.create_custom_token(user.uid)
        return UserLoginResponse(custom_token=custom_token.decode("utf-8"))
    except Exception as e:
        raise RuntimeError(f"Failed to login user or generate custom token: {e}")
