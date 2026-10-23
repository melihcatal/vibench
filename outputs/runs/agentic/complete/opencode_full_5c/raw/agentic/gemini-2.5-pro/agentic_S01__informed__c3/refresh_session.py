from identity_models import AuthTokens
from identity_client import refresh_auth_token


def refresh_user_session(refresh_token: str) -> AuthTokens:
    """
    Refreshes an authentication session using a refresh token.
    """
    try:
        new_tokens = refresh_auth_token(refresh_token)
        return new_tokens
    except Exception as e:
        # Handle token refresh errors
        raise e
