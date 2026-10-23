from identity_client import get_auth_client
from identity_models import AuthResponse


def refresh_session(refresh_token: str) -> AuthResponse:
    auth = get_auth_client()
    try:
        refreshed_user = auth.refresh(refresh_token)
        # The refreshed token response from pyrebase has different keys
        # We need to map them to our AuthResponse model
        response_data = {
            "idToken": refreshed_user["id_token"],
            "refreshToken": refreshed_user["refresh_token"],
            "expiresIn": refreshed_user["expires_in"],
            "localId": refreshed_user["user_id"],
        }
        return AuthResponse(**response_data)
    except Exception as e:
        print(f"An error occurred during session refresh: {e}")
        raise
