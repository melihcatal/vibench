from identity_models import UserCredentials, AuthTokens
from identity_client import sign_in_with_password


def login_user(credentials: UserCredentials) -> AuthTokens:
    """
    Signs in a user with email and password using Firebase Auth REST API.
    """
    try:
        tokens = sign_in_with_password(credentials.email, credentials.password)
        return tokens
    except Exception as e:
        # Handle authentication errors
        raise e
