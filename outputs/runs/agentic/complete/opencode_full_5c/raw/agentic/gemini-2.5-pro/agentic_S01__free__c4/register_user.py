from firebase_admin import auth
from identity_client import get_firebase_app
from identity_models import UserCredentials, AuthResponse


def register_new_user(credentials: UserCredentials) -> AuthResponse:
    get_firebase_app()
    try:
        user_record = auth.create_user(
            email=credentials.email, password=credentials.password
        )
        # Note: Firebase Admin SDK does not return tokens on creation.
        # A client-side sign-in is required to get tokens.
        # This is a simplified representation.
        return AuthResponse(
            id_token="",  # No token returned from admin SDK
            refresh_token="",  # No token returned from admin SDK
            expires_in=0,
            local_id=user_record.uid,
            is_new_user=True,
        )
    except Exception as e:
        raise e
