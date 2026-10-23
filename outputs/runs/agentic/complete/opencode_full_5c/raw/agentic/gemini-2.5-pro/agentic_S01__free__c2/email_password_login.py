from identity_client import get_auth_client
from identity_models import AuthRequest, AuthResponse


def email_password_login(req: AuthRequest) -> AuthResponse:
    auth = get_auth_client()
    try:
        user = auth.sign_in_with_email_and_password(req.email, req.password)
        return AuthResponse(**user)
    except Exception as e:
        print(f"An error occurred during login: {e}")
        raise
