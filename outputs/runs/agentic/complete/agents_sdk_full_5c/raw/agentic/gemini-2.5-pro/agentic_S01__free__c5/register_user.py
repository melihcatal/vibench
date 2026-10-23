from identity_client import get_auth_client
from identity_models import UserRegistration, AuthProviderUser

def register_new_user(user_details: UserRegistration) -> AuthProviderUser:
    """
    Creates a new user account with email and password using Firebase Authentication.
    """
    auth = get_auth_client()
    try:
        user = auth.create_user_with_email_and_password(
            email=user_details.email,
            password=user_details.password
        )
        return AuthProviderUser(
            uid=user['localId'],
            email=user.get('email'),
            id_token=user['idToken'],
            refresh_token=user['refreshToken']
        )
    except Exception as e:
        # In a real app, handle exceptions like email-already-exists
        print(f"Error registering user: {e}")
        raise

