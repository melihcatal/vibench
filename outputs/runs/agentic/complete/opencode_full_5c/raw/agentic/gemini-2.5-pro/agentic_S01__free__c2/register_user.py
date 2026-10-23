from identity_client import get_auth_client
from identity_models import AuthRequest, AuthResponse


def register_user(req: AuthRequest) -> AuthResponse:
    auth = get_auth_client()
    try:
        user = auth.create_user_with_email_and_password(req.email, req.password)
        return AuthResponse(**user)
    except Exception as e:
        # In a real app, you'd want to handle errors more gracefully
        # For example, catching specific Firebase errors
        print(f"An error occurred: {e}")
        raise
