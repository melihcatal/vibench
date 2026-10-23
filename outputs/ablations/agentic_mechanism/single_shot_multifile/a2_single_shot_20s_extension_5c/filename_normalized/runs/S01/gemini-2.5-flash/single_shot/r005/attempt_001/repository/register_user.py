from identity_client import config
from identity_models import RegisterRequest

def register_user(request: RegisterRequest) -> str:
    """
    Creates a new email/password user account using Firebase Authentication.
    Returns the UID of the newly created user.
    """
    try:
        user = config.auth_client.create_user(
            email=request.email,
            password=request.password,
            email_verified=False,
            disabled=False
        )
        return user.uid
    except Exception as e:
        raise RuntimeError(f"Failed to register user: {e}")
