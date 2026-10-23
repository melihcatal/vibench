from identity_client import get_auth_client
from identity_models import UserLogin, AuthProviderUser

def login_with_email_password(credentials: UserLogin) -> AuthProviderUser:
    """
    Signs in a user with their email and password using Firebase Authentication.
    """
    auth = get_auth_client()
    try:
        user = auth.sign_in_with_email_and_password(
            email=credentials.email,
            password=credentials.password
        )
        return AuthProviderUser(
            uid=user['localId'],
            email=user.get('email'),
            id_token=user['idToken'],
            refresh_token=user['refreshToken']
        )
    except Exception as e:
        # In a real app, handle exceptions like invalid-password
        print(f"Error signing in user: {e}")
        raise
