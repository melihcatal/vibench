from identity_client import get_auth_client
from identity_models import SessionRefresh, RefreshedSession

def refresh_user_session(session: SessionRefresh) -> RefreshedSession:
    """
    Refreshes a user's ID token using a refresh token with Firebase Authentication.
    """
    auth = get_auth_client()
    try:
        refreshed_data = auth.refresh(session.refresh_token)
        return RefreshedSession(
            id_token=refreshed_data['idToken'],
            refresh_token=refreshed_data['refreshToken'],
            user_id=refreshed_data['userId']
        )
    except Exception as e:
        # In a real app, handle exceptions like token-expired
        print(f"Error refreshing session: {e}")
        raise
