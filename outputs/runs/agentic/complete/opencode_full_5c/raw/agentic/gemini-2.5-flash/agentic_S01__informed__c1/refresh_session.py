from identity_client import firebase_auth
from identity_models import TokenRefreshRequest, TokenRefreshResponse


def refresh_session(request: TokenRefreshRequest) -> TokenRefreshResponse:
    """
    Refreshes a user session by generating a new custom Firebase token.
    This mimics a server-side session refresh, where a client might
    present an identifier (like UID) and receive a new custom token to
    re-authenticate or get new client-side tokens.
    """
    try:
        # Verify user existence
        user = firebase_auth.get_user(request.uid)
        # Generate a new custom token for the user
        custom_token = firebase_auth.create_custom_token(user.uid)
        return TokenRefreshResponse(custom_token=custom_token.decode("utf-8"))
    except Exception as e:
        raise RuntimeError(f"Failed to refresh session or generate custom token: {e}")
